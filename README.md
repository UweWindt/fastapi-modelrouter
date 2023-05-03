# fastAPI-modelrouter

## create fastAPI CRUD route from SqlAlchemy model

### Installation
```
pip install fastapi-modelrouter
```

### Basic Usage
```
app = FastAPI()
router=ModelRouter(Project, get_db, prefix="/project")
app.include_router(router)
```



- autogenerate Pydantic Basemodels
- Simple to Use
- composite primary key

### Under development

### Todo's
- modelrouter Tests
- Example
- Documentation
- pip package
