from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is running!"}


def test_analyze_endpoint():
    # Giả lập gửi 1 request chứa câu "rất tốt"
    payload = {"text": "sản phẩm này rất tốt"}
    response = client.post("/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["original_text"] == "sản phẩm này rất tốt"
    assert data["sentiment"] == "Positive"