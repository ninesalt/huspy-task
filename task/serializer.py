from django.db.models import Q
from rest_framework import serializers
from task.models import Edge


class EdgeSerializer(serializers.Serializer):
    From = serializers.CharField()
    To = serializers.CharField()

    def has_edge(self, start, end):
        edge = Edge.objects.filter(
            Q(start_node=start, end_node=end) | Q(start_node=end, end_node=start)
        )
        return edge.exists()

    def validate(self, data):
        start = data["From"]
        end = data["To"]
        if self.has_edge(start, end):
            raise serializers.ValidationError(
                f"An edge already exists between nodes {start} and {end}"
            )
        return {"start_node": start, "end_node": end}
