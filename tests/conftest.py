from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app


@pytest.fixture
def session() -> Iterator[Session]:
    """A fresh in-memory SQLite database for every test."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """A TestClient wired to the in-memory `session`. Does not start a real server."""
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_event(client: TestClient):
    """Create an event through the API and return its JSON. Override any field via kwargs."""

    def _make(**overrides) -> dict:
        payload = {
            "title": "Hack Night",
            "location": "Room 110",
            "starts_at": "2030-11-18T18:00:00",
            "capacity": 50,
        } | overrides
        response = client.post("/events", json=payload)
        assert response.status_code == 201, response.text
        return response.json()

    return _make


@pytest.fixture
def make_member(client: TestClient):
    """Create a member through the API and return its JSON. Override any field via kwargs."""
    counter = 0

    def _make(**overrides) -> dict:
        nonlocal counter
        counter += 1
        payload = {"name": f"Member {counter}", "email": f"m{counter}@example.com", "year": 2}
        response = client.post("/members", json=payload | overrides)
        assert response.status_code == 201, response.text
        return response.json()

    return _make
