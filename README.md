# fastapi-modelrouter

## FastAPI Router that creates CRUD routes for SqlAlchemy models

### Features

- Generates direct from SqlAlchemy Models CRUD routes
- no need to write Pydantic Basemodels
- keep SqlAlchemy Models and routes in sync
- Simple to Use
- Supports composite primary keys
- Supports queryparams


## Installation
```
pip install fastapi-modelrouter
```

## Basic Usage
```
from fastapi import FastAPI
from modelrouter import ModelRouter

# setup Sqlalchemy Database
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

sqlalchemy_database_url = "sqlite:///:memory"

engine = create_engine(
    sqlalchemy_database_url, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define Project Model
class Project(Base):
    __tablename__ = 'project'
    projectno = Column(String, primary_key=True)
    project = Column(String)
    state = Column(Integer, default=0)
    owner = Column(String)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# Database session function
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Create FastApi
app = FastAPI()

# Create and include Modelrouter 
app.include_router(ModelRouter(Project, get_db))
```






