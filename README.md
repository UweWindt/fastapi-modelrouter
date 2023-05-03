# fastapi-modelrouter

## create fastAPI Router from a SqlAlchemy model


### Usage

```
app = FastAPI()

app.include_router(ModelRouter(Project, get_db, prefix="/project", ))

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
