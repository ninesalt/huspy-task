from django.contrib import admin
from django.urls import path
from task.views import EdgeAPI, PathAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("connectNode", EdgeAPI.as_view()),
    path("path", PathAPI.as_view()),
]
