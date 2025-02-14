from fastapi.testclient import TestClient  # type: ignore


def test_client(client):
    assert type(client) == TestClient