import logging

from task.models import Edge
from task.serializer import EdgeSerializer
from task.shortest_path import get_shortest_path
from rest_framework import generics
from rest_framework.response import Response


class EdgeAPI(generics.CreateAPIView):
    serializer_class = EdgeSerializer

    def post(self, request, *args, **kwargs):
        # given two nodes in the body, add them to the graph
        # if an edge between them does not already exist
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        logging.info(f"Adding a new edge between nodes {data}")
        Edge(**data).save()
        return Response(status=201)


class PathAPI(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # given two nodes in the params
        # find the shortest path between them

        params = request.query_params
        from_node = params.get("from")
        to_node = params.get("to")

        if not from_node or not to_node:
            return Response("Params must contain to and from nodes", status=422)

        edges = Edge.objects.all()
        edges_tuple = []
        nodes_set = set()

        for e in edges:
            edges_tuple.append((e.start_node, e.end_node))
            nodes_set.add(e.start_node)
            nodes_set.add(e.end_node)

        if from_node not in nodes_set:
            return Response(f"node {from_node} is not in graph", status=422)

        if to_node not in nodes_set:
            return Response(f"node {to_node} is not in graph", status=422)

        path = get_shortest_path(edges_tuple, from_node, to_node)

        if path:
            path_joined = ", ".join(path)
            return Response({"Path": path_joined})

        return Response({"Path": "NO_PATH"})
