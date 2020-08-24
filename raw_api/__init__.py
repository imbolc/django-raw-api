from functools import wraps
from json import loads
from typing import Any, Dict, Union

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, JsonResponse

from trafaret import DataError
from trafaret.constructor import construct

JSON_PARAMS = (
    {"indent": 4, "ensure_ascii": False, "sort_keys": True}
    if settings.DEBUG
    else {}
)


def middleware(get_response):
    """Adds `request.json` attribute and encodes string / dict responses"""

    def _middleware(request: HttpRequest) -> HttpResponse:
        _add_json_property(request)
        response = get_response(request)

        if (
            isinstance(response, tuple)
            and len(response) == 2
            and isinstance(response[1], int)
        ):
            data, status = response
        else:
            data, status = response, 200
        if isinstance(data, (str, dict)):
            return _to_response(data, status)

        return response

    return _middleware


def _add_json_property(request: HttpRequest) -> None:
    """Adds `json` property into a request"""
    cached = None

    @property  # type: ignore
    def json(self):
        nonlocal cached
        if cached is None:
            try:
                cached = loads(request.body.decode("utf-8"))
            except Exception:
                raise SuspiciousOperation("Invalid JSON")
        return cached

    @json.setter
    def json(self, val):
        nonlocal cached
        cached = val

    cls = type(request)
    cls = type(cls.__name__, (cls,), {})
    request.__class__ = cls
    setattr(cls, "json", json)


def _to_response(
    data: Union[str, Dict[str, Any]], status: int
) -> HttpResponse:
    """Encodes data and status into django `HttpResponse`"""
    if isinstance(data, str):
        return HttpResponse(data, status=status, content_type="text/plain")
    return JsonResponse(data, status=status, json_dumps_params=JSON_PARAMS)


def validate_json(validator):
    validate = construct(validator)

    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            if request.method not in ["POST", "PATCH"]:
                return {"message": "Method not allowed"}, 405
            try:
                request.json = validate(request.json)
            except DataError as e:
                return {"message": "Bad request", "errors": e.as_dict()}, 400
            return f(request, *args, **kwargs)

        return wrapper

    return decorator


def validate_query(validator):
    validate = construct(validator)

    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            try:
                request.query = validate(request.GET)
            except DataError as e:
                return {"message": "Bad request", "errors": e.as_dict()}, 400
            return f(request, *args, **kwargs)

        return wrapper

    return decorator


def user_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {"message": "You have to log in"}, 403
        return f(request, *args, **kwargs)

    return wrapper


def staff_required(f):
    @wraps(f)
    @user_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return {"message": "Staff member required"}, 403
        return f(request, *args, **kwargs)

    return wrapper
