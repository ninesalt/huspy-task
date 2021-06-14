from django.contrib import admin
from django.urls import path
from task.views import EdgeAPI

urlpatterns = [path("admin/", admin.site.urls), path("connectNode", EdgeAPI.as_view())]
