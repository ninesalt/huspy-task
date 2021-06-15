import pytest


@pytest.mark.django_db
def test_get_path_simple(client, build_dummy_graph):
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    build_dummy_graph(edges)

    start = "A"
    end = "C"
    response = client.get(f"/path?from={start}&to={end}")
    assert response.status_code == 200
    path = response.json()["Path"]
    assert path == "A, B, C"


@pytest.mark.django_db
def test_get_path_complex(client, build_dummy_graph):
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "F"), ("F", "Z")]
    build_dummy_graph(edges)

    start = "A"
    end = "Z"
    response = client.get(f"/path?from={start}&to={end}")
    assert response.status_code == 200
    path = response.json()["Path"]
    assert path == "A, D, F, Z"


@pytest.mark.django_db
def test_get_no_path(client, build_dummy_graph):
    edges = [("A", "B"), ("B", "C"), ("E", "D")]
    build_dummy_graph(edges)

    start = "A"
    end = "D"
    response = client.get(f"/path?from={start}&to={end}")
    assert response.status_code == 200
    path = response.json()["Path"]
    assert path == "NO_PATH"


@pytest.mark.django_db
def test_get_invalid_node(client, build_dummy_graph):
    edges = [("A", "B"), ("B", "C"), ("E", "D")]
    build_dummy_graph(edges)
    start = "F"
    end = "D"
    response = client.get(f"/path?from={start}&to={end}")
    assert response.status_code == 422
    assert "F is not in graph" in response.json()


@pytest.mark.django_db
def test_get_missing_params(client, build_dummy_graph):
    edges = [("A", "B"), ("B", "C"), ("E", "D")]
    build_dummy_graph(edges)
    start = "F"
    end = "D"
    response = client.get(f"/path?to={end}")
    assert response.status_code == 422
    assert "must contain to and from nodes" in response.json()
