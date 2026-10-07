"""Тесты API-калькулятора."""
from fastapi.testclient import TestClient
from calculator.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_add():
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_subtract():
    response = client.get("/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 6.0


def test_multiply():
    response = client.get("/multiply?a=3&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 12.0


def test_divide():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_divide_by_zero():
    response = client.get("/divide?a=1&b=0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Деление на ноль недопустимо"


def test_power():
    response = client.get("/power?a=2&b=10")
    assert response.status_code == 200
    assert response.json()["result"] == 1024.0


def test_sqrt():
    response = client.get("/sqrt?a=16")
    assert response.status_code == 200
    assert response.json()["result"] == 4.0


def test_sqrt_negative():
    response = client.get("/sqrt?a=-1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Нельзя извлечь корень из отрицательного числа"


def test_calculate_post_add():
    response = client.post("/calculate", json={"operation": "add", "a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_calculate_post_divide_by_zero():
    response = client.post("/calculate", json={"operation": "divide", "a": 1, "b": 0})
    assert response.status_code == 400


def test_calculate_post_sqrt():
    response = client.post("/calculate", json={"operation": "sqrt", "a": 25})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0