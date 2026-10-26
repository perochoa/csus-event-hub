def test_create_event_returns_201_with_id(client):
    response = client.post(
        "/events",
        json={
            "title": "Intro to Git",
            "location": "Lab 105",
            "starts_at": "2030-09-17T18:00:00",
            "capacity": 40,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["title"] == "Intro to Git"
    assert body["capacity"] == 40


def test_create_event_with_zero_capacity_returns_422(client):
    response = client.post(
        "/events",
        json={
            "title": "X",
            "location": "Room 110",
            "starts_at": "2030-01-01T10:00:00",
            "capacity": 0,
        },
    )

    assert response.status_code == 422


def test_create_event_without_title_returns_422(client):
    response = client.post(
        "/events",
        json={"location": "Room 110", "starts_at": "2030-01-01T10:00:00", "capacity": 10},
    )

    assert response.status_code == 422


def test_list_events_orders_by_start_time(client, make_event):
    make_event(title="Later", starts_at="2030-12-01T18:00:00")
    make_event(title="Sooner", starts_at="2030-10-01T18:00:00")

    response = client.get("/events")

    assert response.status_code == 200
    assert [e["title"] for e in response.json()] == ["Sooner", "Later"]


def test_get_event_returns_event(client, make_event):
    event = make_event(title="Resume Review")

    response = client.get(f"/events/{event['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Resume Review"


def test_get_missing_event_returns_404(client):
    response = client.get("/events/999")

    assert response.status_code == 404


def test_update_event_changes_only_given_fields(client, make_event):
    event = make_event(title="Hack Night", capacity=50)

    response = client.patch(f"/events/{event['id']}", json={"capacity": 75})

    assert response.status_code == 200
    assert response.json()["capacity"] == 75
    assert response.json()["title"] == "Hack Night"


def test_update_missing_event_returns_404(client):
    response = client.patch("/events/999", json={"capacity": 10})

    assert response.status_code == 404


def test_delete_event_removes_it(client, make_event):
    event = make_event()

    response = client.delete(f"/events/{event['id']}")

    assert response.status_code == 204
    assert client.get(f"/events/{event['id']}").status_code == 404
