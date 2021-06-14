import pytest


@pytest.mark.django_db
def test_add_edge(client):
    body = {"From": "A", "To": "B"}
    response = client.post("/connectNode", body, content_type="application/json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_add_missing_node(client):
    response = client.post("/connectNode", {}, content_type="application/json")
    assert response.status_code == 400
    v = "This field is required."
    assert v == response.json()["From"][0]
    assert v == response.json()["To"][0]


@pytest.mark.django_db
def test_add_duplicate_edge(client):
    body = {"From": "A", "To": "B"}
    # add edge from A to B
    client.post("/connectNode", body, content_type="application/json")

    # add same edge again (should fail)
    response = client.post("/connectNode", body, content_type="application/json")
    assert "already exists" in response.json()["non_field_errors"][0]
    assert response.status_code == 400

    # add reverse edge again (should fail)
    body = {"From": "B", "To": "A"}
    response = client.post("/connectNode", body, content_type="application/json")
    assert "already exists" in response.json()["non_field_errors"][0]
    assert response.status_code == 400
