from task.models import Edge
import pytest


@pytest.fixture
def build_dummy_graph():
    def create_func(edges):
        entries = [Edge(start_node=e[0], end_node=e[1]) for e in edges]
        Edge.objects.bulk_create(entries)

    return create_func
