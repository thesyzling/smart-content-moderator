import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_text_moderation():
    response = client.post("/api/v1/moderate/text", json={"email": "pytest@example.com", "text": "pytest message"})
    assert response.status_code in (200, 409)
    if response.status_code == 200:
        data = response.json()
        assert "classification" in data
        assert "confidence" in data

def test_image_moderation():
    response = client.post("/api/v1/moderate/image", json={"email": "pytest@example.com", "image_url": "https://via.placeholder.com/150"})
    assert response.status_code in (200, 409)
    if response.status_code == 200:
        data = response.json()
        assert "classification" in data
        assert "confidence" in data

def test_analytics():
    response = client.get("/api/v1/moderate/analytics/summary?user=pytest@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
