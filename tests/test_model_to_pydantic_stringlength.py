from sqlalchemy import Column, String,Integer, create_engine
from sqlalchemy.orm import declarative_base

from src.modelrouter.model_to_pydantic import model_to_pydantic

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


class String80(Base):
    __tablename__ = 'string80'
    pk = Column(String(70), primary_key=True)
    str80 = Column(String(80), primary_key=True)
    simple = Column(String,  nullable=True,default="xxx")
    num = Column(Integer, nullable=True, default=2)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def test_maxlength():
    SchemaTest = model_to_pydantic(String80)

    assert SchemaTest.schema() == {
        "title": "String80",
        "type": "object",
        "properties": {
            "pk": {"title": "Pk", "type": "string", "maxLength": 70},
            "str80": {"title": "Str80", "type": "string", "maxLength": 80},
            "simple": {"title": "Simple", "type": "string"},
            "num": {"title": "Num", "type": "integer"},
        },
        "required": ["pk", "str80"]
    }
