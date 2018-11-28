from django.urls import path

import views

urlpatterns = [
    path("dict", views.dict_response),
    path("tuple", views.tuple_response),
    path("django-response", views.django_response),
    path("request-json", views.request_json),
    path("require-user", views.require_user),
    path("require-staff", views.require_staff),
    path("query-validation", views.query_validation),
    path("json-validation", views.json_validation),
]
