# fastapi-modelrouter

## FastAPI Router that creates CRUD routes for SqlAlchemy models

### Installation
```
pip install fastapi-modelrouter
```

### Basic Usage
```
app = FastAPI()
router=ModelRouter(Project, get_db)
app.include_router(router)
```



- autogenerate Pydantic Basemodels
- Simple to Use
- composite primary key

### Under development


