from typing import Container, Optional, Type, Any

from pydantic import BaseConfig, BaseModel, create_model
from pydantic.fields import FieldInfo
from sqlalchemy.inspection import inspect


class OrmConfig(BaseConfig):
    orm_mode = True


def model_to_pydantic(
        model: Type,
        *,
        name: str = '',
        exclude: Container[str] = (),
        only: Container[str] = (),
        only_pk: bool = False,
        exclude_pk: bool = False,
        force_optional=False

) -> Type[BaseModel]:
    """

        Args:
            model: SqlAlchemy model
            name:  Optional: if name=="" the name of the Model will used
            exclude: List of fields that are excluded
            only:    List of fields
            only_pk: if True generates Schema only for primary key fields
            exclude_pk: If True generate Schema for non pk fields
            force_optional: Make all fields optional
        Returns:
           Pydantic BaseModel
        """
    mapper: Any = inspect(model)
    fields = {}
    for column in mapper.columns:
        if exclude and column.name in exclude:
            continue
        if only and column.name not in only:
            continue
        if only_pk and not column.primary_key:
            continue
        if exclude_pk and column.primary_key:
            continue
        python_type: Optional[type] = None
        if hasattr(column.type, "impl"):
            if hasattr(column.type.impl, "python_type"):
                python_type = column.type.impl.python_type
        elif hasattr(column.type, "python_type"):
            python_type = column.type.python_type
        assert python_type, f"Could not infer python_type for {column}"
        default = None
        if not force_optional:
            if column.default is None and not column.nullable:
                default = ...
            # else:
            #     default = column.default
        if hasattr(column.type, "length") and column.type.length:
            fields[column.name] = (python_type, FieldInfo(max_length=column.type.length, default=default))
        else:
            fields[column.name] = (python_type, default)
    basemodel_name = name if name != '' else model.__name__
    basemodel: Type[BaseModel] = create_model(basemodel_name, __config__=OrmConfig, **fields)  # type: ignore
    return basemodel
