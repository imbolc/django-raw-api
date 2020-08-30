from django.urls import path

import views

urlpatterns = [
    path("dict-response", views.dict_response),
    path("async/dict-response", views.async_dict_response),
    path("string-response", views.string_response),
    path("async/string-response", views.async_string_response),
    path("tuple-dict-response", views.tuple_dict_response),
    path("async/tuple-dict-response", views.async_tuple_dict_response),
    path("tuple-string-response", views.tuple_string_response),
    path("async/tuple-string-response", views.async_tuple_string_response),
    path("django-response", views.django_response),
    path("async/django-response", views.async_django_response),
    path("request-json", views.request_json),
    path("async/request-json", views.async_request_json),
    path("require-user", views.require_user),
    path("async/require-user", views.async_require_user),
    path("require-staff", views.require_staff),
    path("async/require-staff", views.async_require_staff),
    path("query-validation", views.query_validation),
    path("async/query-validation", views.async_query_validation),
    path("json-validation", views.json_validation),
    path("async/json-validation", views.async_json_validation),
]
