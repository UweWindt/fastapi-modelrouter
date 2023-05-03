
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base





sqlalchemy_database_url = "sqlite:///test.db"

engine = create_engine(
    sqlalchemy_database_url, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Part(Base):
    __tablename__ = 'part'
    partno = Column(String, primary_key=True)
    partname = Column(String)
    specification = Column(String)


class Project(Base):
    __tablename__ = 'project'
    projectno = Column(String, primary_key=True)
    project = Column(String)
    state = Column(Integer, default=0)
    owner = Column(String)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()
