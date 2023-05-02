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


def test_simple_model() -> None:
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
