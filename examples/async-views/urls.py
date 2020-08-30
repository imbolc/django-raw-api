from django.contrib import admin
from django.urls import path

import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("query", views.query),
    path("json", views.json),
    path("user", views.user),
    path("staff", views.staff),
]
