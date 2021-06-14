from django.db import models

# The graph here is a simplified data structure
# meant to represent the connections between all the nodes
# since its undirected, every row will represent an edge
class Edge(models.Model):
    start_node = models.CharField(max_length=10)
    end_node = models.CharField(max_length=10)
