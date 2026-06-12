from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_state_returns_world_and_organisms():
    response = client.get("/api/simulation/state")
    assert response.status_code == 200

    data = response.json()
    assert data["width"] == 16
    assert data["height"] == 16
    assert len(data["tiles"]) == 16 * 16
    assert len(data["organisms"]) > 0


def test_step_advances_tick():
    before = client.get("/api/simulation/state").json()["tick"]

    response = client.post("/api/simulation/step")
    assert response.status_code == 200

    after = response.json()["tick"]
    assert after == before + 1


def test_reset_with_custom_population():
    response = client.post("/api/simulation/reset", json={"population_size": 5, "mutation_rate": 0.1, "food_regen_multiplier": 1.0})
    assert response.status_code == 200

    data = response.json()
    assert data["tick"] == 0
    assert len(data["organisms"]) == 5
