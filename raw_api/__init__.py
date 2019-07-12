from json import loads
from functools import wraps

from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.conf import settings

from trafaret import DataError
from trafaret.constructor import construct


JSON_PARAMS = (
    {"indent": 4, "ensure_ascii": False, "sort_keys": True}
    if settings.DEBUG
    else {}
)


def middleware(get_response):
    """Add `request.json` attribute and encode response into json"""

    def add_json_property(request):
        cached = None

        @property
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

    def _middleware(request):
        add_json_property(request)
        response = get_response(request)
        if isinstance(response, dict):
            return JsonResponse(response, json_dumps_params=JSON_PARAMS)
        if isinstance(response, tuple) and len(response) == 2:
            data, status = response
            return JsonResponse(
                data, status=status, json_dumps_params=JSON_PARAMS
            )
        return response

    return _middleware


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
