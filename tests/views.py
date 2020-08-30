from asgiref.sync import sync_to_async
from django.contrib.auth import get_user
from django.http import HttpResponse

from raw_api import (
    staff_required,
    user_required,
    validate_json,
    validate_query,
)


def dict_response(request):
    return {"hello": "world"}


async def async_dict_response(request):
    return {"hello": "world"}


def string_response(request):
    return "hey"


async def async_string_response(request):
    return "hey"


def tuple_dict_response(request):
    return {"bad": "request"}, 400


async def async_tuple_dict_response(request):
    return {"bad": "request"}, 400


def tuple_string_response(request):
    return "bad request", 400


async def async_tuple_string_response(request):
    return "bad request", 400


def django_response(request):
    return HttpResponse("foo")


async def async_django_response(request):
    return HttpResponse("foo")


def request_json(request):
    return request.json


async def async_request_json(request):
    return request.json


@user_required
def require_user(request):
    return {"user": request.user.username}


@user_required
async def async_require_user(request):
    return {"user": request.user.username}


@staff_required
def require_staff(request):
    return {"user": request.user.username}


@staff_required
async def async_require_staff(request):
    return {"user": request.user.username}


@validate_query({"id": int})
def query_validation(request):
    return request.query


@validate_query({"id": int})
async def async_query_validation(request):
    return request.query


@validate_json({"id": int})
def json_validation(request):
    return request.json


@validate_json({"id": int})
async def async_json_validation(request):
    return request.json
