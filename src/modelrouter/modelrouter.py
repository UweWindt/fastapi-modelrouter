from enum import Enum
from typing import Any, Optional, List, Sequence, Union, Callable, Type

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.types import DecoratedCallable
from pydantic import BaseModel
from sqlalchemy import Column, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, DeclarativeMeta as Model

from .model_to_pydantic import model_to_pydantic

CALLABLE_SESSION = Callable[..., Session]
CALLABLE_MODEL = Callable[..., Model]
CALLABLE_LIST = Callable[..., List[Model]]
DEPENDENCIES = Optional[Sequence[Depends]]
NOT_FOUND = HTTPException(404, "Item not found")


class ModelRouter(APIRouter):

    def __init__(
            self,
            db_model: Type[Model],
            db: CALLABLE_SESSION,
            prefix: str = "",
            tags: Optional[List[Union[str, Enum]]] = None,
            get_all_route: bool = True,
            get_one_route: bool = True,
            create_route: bool = True,
            update_route: bool = True,
            delete_one_route: bool = True,
            **kwargs: Any
    ) -> None:
        """

        :param db_model: SqlAlchemy model
        :param db: function to get the db.session
        :param prefix:
        :param tags:
        :param get_all_route:
        :param get_one_route:
        :param create_route:
        :param update_route:
        :param delete_one_route:
        :param kwargs:
        """
        self.db_model: Type[Model] = db_model
        self.db: CALLABLE_SESSION = db
        self.schema: Type[BaseModel] = model_to_pydantic(db_model)
        self.queryparams_schema: Type[BaseModel] = model_to_pydantic(db_model,
                                                                     name=db_model.__name__ + 'queryParams',
                                                                     force_optional=True)
        self.create_schema: Type[BaseModel] = model_to_pydantic(db_model,
                                                                name=db_model.__name__ + '_Create')
        self.pk_schema: Type[BaseModel] = model_to_pydantic(db_model,
                                                            name=db_model.__name__ + '_Primary_Key',
                                                            only_pk=True)
        self.nonpk_schema: Type[BaseModel] = model_to_pydantic(db_model,
                                                               name=db_model.__name__ + '_Body',
                                                               exclude_pk=True)

        prefix = prefix if prefix != "" else "/" + db_model.__name__.lower()
        print(prefix)
        super().__init__(prefix=prefix, tags=tags, **kwargs)

        if get_all_route:
            self._add_api_route(
                "",
                self._get_all(),
                methods=["GET"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Get All",
                # dependencies=get_all_route,
            )

        if get_one_route:
            self._add_api_route(
                self.pk_parameter_string(),
                self._get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
                # dependencies=get_one_route,
                error_responses=[NOT_FOUND],
            )

        if create_route:
            self._add_api_route(
                "",
                self._create(),
                methods=["POST"],
                response_model=self.schema,
                summary="Create One",
                # dependencies=create_route,
            )

        if update_route:
            self._add_api_route(
                self.pk_parameter_string(),
                self._update(),
                methods=["PUT"],
                response_model=self.schema,
                summary="Update One",
                # dependencies=update_route,
                error_responses=[NOT_FOUND],
            )

        if delete_one_route:
            self._add_api_route(
                self.pk_parameter_string(),
                self._delete_one(),
                methods=["DELETE"],
                response_model=self.schema,
                summary="Delete One",
                # dependencies=delete_one_route,
                error_responses=[NOT_FOUND],
            )

        # End of __init__

    def pk_parameter_string(self):
        rv = ""
        mapper: Any = inspect(self.db_model)
        for c in mapper.columns:
            if c.primary_key:
                rv += "/{" + c.name + "}"
        return rv

    def _add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            error_responses: Optional[List[HTTPException]] = None,
            **kwargs: Any,
    ) -> None:
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        super().add_api_route(
            path,
            endpoint,
            # dependencies=dependencies,
            responses=responses,
            **kwargs
        )

    def get(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                    route.path == f"{self.prefix}{path}"  # type: ignore
                    and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    #

    def _get_all(self) -> Callable[[Session, BaseModel], list[Type[Model]]]:

        def queryfilter(queryparams):
            params = queryparams.dict()
            return [Column(key) == params[key] for key in params if params[key] is not None]

        def route(
                db=Depends(self.db),
                queryparams=Depends(self.queryparams_schema),
        ) -> List[Type[Model]]:
            db_models: List[Type[Model]] = (
                db.query(self.db_model)  # type:ignore
                .filter(and_(True, *queryfilter(queryparams)))  # type:ignore
                # .order_by(getattr(self.db_model, self._pk))
                # .limit(limit)
                # .offset(skip)
                .all()
            )
            return db_models

        return route  # type:ignore

    def _get_one(self) -> CALLABLE_MODEL:

        def route(
                db: Session = Depends(self.db),  # type:ignore
                pkfields=Depends(self.pk_schema)  # type:ignore
        ) -> Model:

            model: Model = db.get(self.db_model, pkfields.dict().values())  # type:ignore
            if model:
                return model
            else:
                raise NOT_FOUND from None

        return route

    def _create(self) -> CALLABLE_MODEL:
        def route(
                model: self.create_schema,  # type: ignore
                db: Session = Depends(self.db),  # type: ignore
        ) -> Model:
            try:
                db_model: Model = self.db_model(**model.dict())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route

    def _update(self) -> CALLABLE_MODEL:
        def route(
                data: self.nonpk_schema,  # type: ignore
                pkfields=Depends(self.pk_schema),  # type:ignore
                db: Session = Depends(self.db)  # type:ignore
        ) -> Model:
            model: Model = db.get(self.db_model, pkfields.dict().values())  # type:ignore
            try:
                for key, value in data.dict().items():
                    if hasattr(model, key):
                        setattr(model, key, value)
                db.commit()
                db.refresh(model)
                return model
            except IntegrityError as e:
                db.rollback()
                self._raise(e)
            return model  # only because of mypy

        return route

    def _delete_one(self) -> CALLABLE_MODEL:

        def route(
                pkfields=Depends(self.pk_schema),
                db: Session = Depends(self.db)  # type:ignore
        ) -> Model:
            model: Model = db.get(self.db_model, pkfields.dict().values())  # type:ignore
            if model:
                db.delete(model)
                db.commit()
                return model
            else:
                raise NOT_FOUND from None

        return route

    def _raise(self, e: Exception, status_code: int = 422) -> HTTPException:
        raise HTTPException(422, ", ".join(e.args)) from e
