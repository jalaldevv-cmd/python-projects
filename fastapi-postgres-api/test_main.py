import os
import pytest

os.environ["ENV_FILE"] = ".env.test"

from fastapi.testclient import TestClient
from database import get_connection
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products")
    connection.commit()

    cursor.close()
    connection.close()

def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200

def test_get_product_not_found():
    response = client.get("/products/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Test Keyboard",
            "price": 1500,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Product successfully created",
        "name": "Test Keyboard",
        "price": 1500,
        }