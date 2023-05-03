from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base

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


def test_simple():
    assert 2 == 2
