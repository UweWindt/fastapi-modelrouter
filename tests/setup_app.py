from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base


def setup_app():
    app = FastAPI()
    return app


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


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()
