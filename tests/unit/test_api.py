from fastapi.testclient import TestClient

import app.main as main
from app.services.llm.schemas import LLMResponse

client = TestClient(main.app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to SupportOps AI",
        "status": "running",
    }


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {"status": "healthy"}


def test_chat_endpoint(monkeypatch):

    async def mock_generate_response(message: str):

        return LLMResponse(
            text=f"Mocked response for: {message}",
            provider="openai",
            model="gpt-4.1-mini",
        )

    monkeypatch.setattr(
        main,
        "generate_response",
        mock_generate_response,
    )

    response = client.post(
        "/chat",
        json={
            "message": "Where is my order?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == (
        "Mocked response for: Where is my order?"
    )

    assert data["provider"] == "openai"
    assert data["model"] == "gpt-4.1-mini"

def test_chat_rejects_empty_message():

    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_rejects_missing_message():

    response = client.post("/chat", json={})

    assert response.status_code == 422
