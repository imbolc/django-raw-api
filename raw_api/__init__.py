import json
from functools import wraps

from django.http import JsonResponse
from django.utils.functional import SimpleLazyObject
from django.core.exceptions import SuspiciousOperation

from trafaret import DataError
from trafaret.constructor import construct


def middleware(get_response):
    """Add `request.json` attribute and encode response into json"""

    def load_json(request):
        try:
            return json.loads(request.body.decode("utf-8"))
        except Exception:
            raise SuspiciousOperation("Invalid JSON")

    def _middleware(request):
        request.json = SimpleLazyObject(lambda: load_json(request))
        response = get_response(request)
        if isinstance(response, dict):
            return JsonResponse(response)
        if isinstance(response, tuple) and len(response) == 2:
            data, status = response
            return JsonResponse(data, status=status)
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
