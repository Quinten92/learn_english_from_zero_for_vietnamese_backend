from fastapi.testclient import TestClient
# Adjust the import path based on the project structure
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Learn English API"}

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"name": "Item Foo"}, {"name": "Item Bar"}]
