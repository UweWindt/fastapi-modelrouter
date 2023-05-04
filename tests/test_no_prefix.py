from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modelrouter.modelrouter import ModelRouter
from .setup_app import Project, get_db

app = FastAPI()

app.include_router(ModelRouter(Project, get_db ))

client = TestClient(app)

def test_get_project():
    response = client.get("/project")
    assert response.status_code == 200
    assert response.json() == []