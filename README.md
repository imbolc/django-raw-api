django-raw-api
==============
JSON API should be as simple as `dict` and status code :)

Hello world
-----------
```python
from raw_api import validate_json

@validate_json({"name": str})
def hello(request):
    name = request.json["name"]
    if name == "world":
        return "won't work here", 400
    return {"hello": name}
```

Setup
-----
- Install in from pypi: `pip install django-raw-api`
- Add `raw_api.middleware` middleware into `MIDDLEWARE` list of your `settings.py`

API
---

### Middleware
It adds lazy `request.json` attribute and serializes raw responses such as:
- `str` or tuple `(message: str, status: int)` - into plain text response
- `dict` or `(data: dict, status: int)` - into JSON response

### Request

- `request.json` - parsed json
- `request.query` - parsed query (only after `@validate_query`)


### Response
You can just return `str`, `dict` with an optional status code

```python
def hello(request):
    return "hi"


def hello_json(request):
    return {"hello": "world"}


def with_status(request):
    return {"message": "bad request"}, 400
```


### Auth
Decorators `@user_required` and `@staff_required` is analogous to
`@login_required` and  `@staff_member_required` with JSON output instead of
redirecting

```python
from raw_api import staff_required

@staff_required
async def hello(request):
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
async def bar(request):
    assert isinstance(id, int)
    return request.query
```


Tests
-----
```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -Ur requirements-dev.txt
    python -m pytest tests
```

[trafaret]: https://github.com/Deepwalker/trafaret
