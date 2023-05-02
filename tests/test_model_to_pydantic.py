from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base

from modelrouter.model_to_pydantic import model_to_pydantic

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


class Part(Base):
    __tablename__ = 'part'
    partno = Column(String, primary_key=True)
    partname = Column(String)
    specification = Column(String)


Base.metadata.create_all(engine)
LocalSession = sessionmaker(bind=engine)
db: Session = LocalSession()
part = Part(partno="001", partname="Bold", specification="Alpha 1")
db.add(part)
db.commit()


def test_part() -> None:
    SchemaPart = model_to_pydantic(Part)

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partno": {"title": "Partno", "type": "string"},
            "partname": {"title": "Partname", "type": "string"},
            "specification": {"title": "Specification", "type": "string"},
        },
        "required": ["partno"]
    }


def test_part_only_partname() -> None:
    SchemaPart = model_to_pydantic(Part, only=["partname"])

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partname": {"title": "Partname", "type": "string"},
        },

    }


def test_part_exclude_partname() -> None:
    SchemaPart = model_to_pydantic(Part, exclude=["partname"])

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partno": {"title": "Partno", "type": "string"},
            "specification": {"title": "Specification", "type": "string"},
        },
        "required": ["partno"]
    }


def test_part_only_pk() -> None:
    SchemaPart = model_to_pydantic(Part, only_pk=True)

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partno": {"title": "Partno", "type": "string"},
        },
        "required": ["partno"]
    }


def test_part_exclude_pk() -> None:
    SchemaPart = model_to_pydantic(Part, exclude_pk=True)

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partname": {"title": "Partname", "type": "string"},
            "specification": {"title": "Specification", "type": "string"},
        },

    }


def test_part_fore_optional() -> None:
    SchemaPart = model_to_pydantic(Part, force_optional=True)

    assert SchemaPart.schema() == {
        "title": "Part",
        "type": "object",
        "properties": {
            "partno": {"title": "Partno", "type": "string"},
            "partname": {"title": "Partname", "type": "string"},
            "specification": {"title": "Specification", "type": "string"},
        },

    }
