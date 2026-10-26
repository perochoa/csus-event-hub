def test_search_events_matches_title(client, make_event):
    make_event(title="Hack Night")
    make_event(title="Resume Review")

    response = client.get("/events/search", params={"q": "Hack"})

    assert response.status_code == 200
    assert [e["title"] for e in response.json()] == ["Hack Night"]
