import logging

from task.models import Edge
from task.serializer import EdgeSerializer
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
