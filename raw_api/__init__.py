import asyncio
from functools import wraps
from json import loads

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import sync_and_async_middleware
from trafaret import DataError
from trafaret.constructor import construct

JSON_PARAMS = (
    {"indent": 4, "ensure_ascii": False, "sort_keys": True}
    if settings.DEBUG
    else {}
)


@sync_and_async_middleware
def middleware(get_response):
    """Adds `request.json` attribute and encodes str / dict responses"""

    if asyncio.iscoroutinefunction(get_response):

        async def raw_api_middleware(request):
            _add_json_property(request)
            response = await get_response(request)
            return _process_response(response)

    else:

        def raw_api_middleware(request):
            _add_json_property(request)
            response = get_response(request)
            return _process_response(response)

    return raw_api_middleware


def _process_response(response):
    if (
        isinstance(response, tuple)
        and len(response) == 2
        and isinstance(response[1], int)
    ):
        data, status = response
    else:
        data, status = response, 200

    if isinstance(data, str):
        return HttpResponse(data, status=status, content_type="text/plain")
    elif isinstance(data, dict):
        return JsonResponse(data, status=status, json_dumps_params=JSON_PARAMS)
    return response


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


def validate_json(validator):
    validate = construct(validator)

    def decorator(f):
        if asyncio.iscoroutinefunction(f):

            async def wrapper(request, *args, **kwargs):
                return _get_json_error(validate, request) or await f(
                    request, *args, **kwargs
                )

        else:

            def wrapper(request, *args, **kwargs):
                return _get_json_error(validate, request) or f(
                    request, *args, **kwargs
                )

        return wraps(f)(wrapper)

    return decorator


def _get_json_error(validate, request):
    """Returns `None` or an error response"""
    if request.method not in ["POST", "PATCH"]:
        return {"message": "Method not allowed"}, 405
    try:
        request.json = validate(request.json)
    except DataError as e:
        return _data_error_response(e)
    return None


def validate_query(validator):
    validate = construct(validator)

    def decorator(f):
        if asyncio.iscoroutinefunction(f):

            async def wrapper(request, *args, **kwargs):
                return _get_query_error(validate, request) or await f(
                    request, *args, **kwargs
                )

        else:

            def wrapper(request, *args, **kwargs):
                return _get_query_error(validate, request) or f(
                    request, *args, **kwargs
                )

        return wraps(f)(wrapper)

    return decorator


def _get_query_error(validate, request):
    """Returns `None` or an error response"""
    try:
        request.query = validate(request.GET)
    except DataError as e:
        return _data_error_response(e)
    return None


def _data_error_response(e: DataError):
    return {"message": "Bad request", "errors": e.as_dict()}, 400


def user_required(f):
    if asyncio.iscoroutinefunction(f):

        async def wrapper(request, *args, **kwargs):
            if not await sync_to_async(getattr)(
                request.user, "is_authenticated"
            ):
                return _user_error_response
            return await f(request, *args, **kwargs)

    else:

        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return _user_error_response
            return f(request, *args, **kwargs)

    return wraps(f)(wrapper)


_user_error_response = {"message": "You have to log in"}, 403


def staff_required(f):
    if asyncio.iscoroutinefunction(f):

        async def wrapper(request, *args, **kwargs):
            if not request.user.is_staff:
                return _staff_error_response
            return await f(request, *args, **kwargs)

    else:

        def wrapper(request, *args, **kwargs):
            if not request.user.is_staff:
                return _staff_error_response
            return f(request, *args, **kwargs)

    return wraps(f)(user_required(wrapper))


_staff_error_response = {"message": "Staff member required"}, 403
