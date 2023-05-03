from fastapi.testclient import TestClient

from .setup_app import setup_app,Project,get_db
app = setup_app()





client = TestClient(app)


@app.get("/")
def home():
    return {"hello": "world"}

