import pytest
from fastapi.testclient import TestClient

from db_conn.db import Base
from utils.dependencies import get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)


def test_get_classes(client):
    """Test GET /classes endpoint"""
    response = client.get("/api/fitness_classes/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_book_class_validation(client):
    """Test POST /book endpoint validation"""
    # Test invalid email
    response = client.post("/api/fitness_classes/book", json={
        "class_id": 1,
        "user_email": "invalid-email",
        "user_name": "Test User"
    })
    assert response.status_code == 422

    # Test empty name
    response = client.post("/api/fitness_classes/book", json={
        "class_id": 1,
        "user_email": "test@example.com",
        "user_name": ""
    })
    assert response.status_code == 422

    # Test duplicate email
    # it should return error
    # response = client.post("/api/fitness_classes/book", json={
    #     "class_id": 1,
    #     "user_email": "test@example.com",
    #     "user_name": "tester"
    # })
    # assert response.status_code == 422


def test_get_bookings(client):
    """Test GET /bookings endpoint"""
    response = client.get("/api/fitness_classes/bookings?email=test@example.com")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_timezone_conversion(client):
    """Test timezone conversion functionality"""
    # Test with different timezone
    response = client.get("/api/fitness_classes/classes?timezone_param=America/New_York")
    assert response.status_code == 200

    # Test with invalid timezone
    response = client.get("/api/fitness_classes/classes?timezone_param=Invalid/Timezone")
    assert response.status_code == 200  # Should handle gracefully


if __name__ == "__main__":
    pytest.main([__file__])