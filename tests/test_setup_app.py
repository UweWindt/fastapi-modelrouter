from fastapi.testclient import TestClient
from modelrouter.modelrouter import ModelRouter
from .setup_app import setup_app,Part,get_db
app = setup_app()


app.include_router(ModelRouter(Part,get_db,prefix="/part",))


client = TestClient(app)


@app.get("/")
def home():
    return {"hello": "world"}

def test_get_part():
    response = client.get("/part")
    assert response.status_code == 200
    assert response.json() == []