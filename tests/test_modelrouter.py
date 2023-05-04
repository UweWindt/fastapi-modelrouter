from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modelrouter.modelrouter import ModelRouter
from .setup_app import Project, get_db

app = FastAPI()

app.include_router(ModelRouter(Project, get_db, prefix="/project", ))

client = TestClient(app)


def test_get_project():
    response = client.get("/project")
    assert response.status_code == 200
    assert response.json() == []


def test_get_one_project_not_found():
    response = client.get("/project/alpha")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_post_project():
    response = client.post(
        "/project",
        json={"projectno": "alpha"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["projectno"] == "alpha"
    assert data["project"] is None
    assert data["owner"] is None


def test_get_one_project():
    response = client.get("/project/alpha")
    data = response.json()
    assert data["projectno"] == "alpha"
    assert data["project"] is None
    assert data["owner"] is None


def test_put_project():
    response = client.put(
        "/project/alpha",
        json={"project": "123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["projectno"] == "alpha"
    assert data["project"] == "123"


def test_delete_project_not_found():
    response = client.delete(
        "/project/123",
    )
    assert response.status_code == 404
    # response = client.get("/api/project")
    # assert response.status_code == 200
    # assert response.json() == []


def test_delete_project():
    response = client.delete(
        "/project/alpha",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["projectno"] == "alpha"
    assert data["project"] == "123"
