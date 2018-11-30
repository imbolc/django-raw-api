from django.http import HttpResponse

from raw_api import (
    user_required,
    staff_required,
    validate_query,
    validate_json,
)


def dict_response(request):
    return {"hello": "world"}


def tuple_response(request):
    return {"bad": "request"}, 400


def django_response(request):
    return HttpResponse("foo")


def request_json(request):
    return request.json


@user_required
def require_user(request):
    return {"user": request.user.username}


@staff_required
def require_staff(request):
    return {"user": request.user.username}


@validate_query({"id": int})
def query_validation(request):
    return request.query


@validate_json({"id": int})
def json_validation(request):
    return request.json
