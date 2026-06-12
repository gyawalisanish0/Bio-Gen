from fastapi.testclient import TestClient

from app.config import SPECIES_SHAPES
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

    assert len(data["species"]) == len(SPECIES_SHAPES)
    for species in data["species"]:
        assert species["shape"] in SPECIES_SHAPES
        assert 0 <= species["hue"] < 360

    valid_species_ids = {s["id"] for s in data["species"]}
    for organism in data["organisms"]:
        assert organism["species_id"] in valid_species_ids


def test_step_advances_tick():
    before = client.get("/api/simulation/state").json()["tick"]

    response = client.post("/api/simulation/step")
    assert response.status_code == 200

    after = response.json()["tick"]
    assert after == before + 1


def test_reset_with_custom_population():
    response = client.post(
        "/api/simulation/reset",
        json={"population_size": 5, "mutation_rate": 0.1, "food_regen_multiplier": 1.0, "tick_interval_ms": 100},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["tick"] == 0
    assert len(data["organisms"]) == 5
    assert data["tick_interval_ms"] == 100


def test_set_speed_clamps_to_bounds():
    response = client.post("/api/simulation/speed", json={"tick_interval_ms": 5})
    assert response.status_code == 200
    assert response.json()["tick_interval_ms"] == 50

    response = client.post("/api/simulation/speed", json={"tick_interval_ms": 5000})
    assert response.status_code == 200
    assert response.json()["tick_interval_ms"] == 1000
