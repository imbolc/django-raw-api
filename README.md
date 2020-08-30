django-raw-api
==============
[Async][async views]-friendly straightforward Django API helpers

Hello world
-----------
```python
from raw_api import validate_json

@validate_json({"name": str})
def hello(request):
    name = request.json["name"]
    if name == "death":
        return "not today", 403
    return {"hello": request.json["name"]}
```

Setup
-----

- Install in from pypi: `pip install django-raw-api`
- Add `raw_api` into `INSTALLED_APPS` list of your `settings.py`
- Add `raw_api.middleware` middleware into `MIDDLEWARE`

API
---

### Middleware

It adds lazy `request.json` attribute and serializes raw responses such as:
- `str` or `tuple(message: str, status: int)` - into plain text response
- `dict` or `tuple(data: dict, status: int)` - into JSON response

### Request

- `request.json: dict` - parsed json
- `request.query: dict` - parsed query (only after `@validate_query`)


### Response

You can just return `str` or `dict` with an optional status code

```python
def json_200ok(request):
    return {"hello": "world"}


def plain_text_with_status(request):
    return "bad request", 400
```


### Authorization

Decorators `@user_required` and `@staff_required` is analogous to
`@login_required` and  `@staff_member_required` with JSON-based errors instead
of redirecting

Both decorators cache `request.user` so you can use it without `sync_to_async`
even in async views.

```python
from raw_api import user_required, staff_required

@user_required
async def user(request):
    # no `sync_to_async` required
    return request.user.username

@staff_required
def staff(request):
    return {"admin": "zone"}
```


Data validation
---------------
`@validate_query` and `@validate_json` decorators are there to perform simple
first-level validation of requests data. Internally they use the [trafaret][]
library.

```python
from raw_api import validate_json, validate_query

@validate_json({"ids": [int], "hello?": str})
async def foo(request):
    return request.json

@validate_query({"id": int})
def bar(request):
    assert isinstance(id, int)
    return request.query
```

Examples
--------

There's an example of using it with [async views][] in the `examples` folder.

Tests
-----
```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -Ur requirements-dev.txt
    python -m pytest tests
```

[async views]: https://docs.djangoproject.com/en/3.1/topics/async/#async-views
[trafaret]: https://github.com/Deepwalker/trafaret
