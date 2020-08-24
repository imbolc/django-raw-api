from django.urls import path

import views

urlpatterns = [
    path("dict-response", views.dict_response),
    path("string-response", views.string_response),
    path("tuple-dict-response", views.tuple_dict_response),
    path("tuple-string-response", views.tuple_string_response),
    path("django-response", views.django_response),
    path("request-json", views.request_json),
    path("require-user", views.require_user),
    path("require-staff", views.require_staff),
    path("query-validation", views.query_validation),
    path("json-validation", views.json_validation),
]
