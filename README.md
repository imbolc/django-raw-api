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
        return {"message": "too corny"}, 400
    return {"hello": name}
```

Setup
-----
- Install in from pypi: `pip install raw_api`
- Add `raw_api.middleware` middleware into `MIDDLEWARE` list of your `settings.py`

API
---
### Middleware
It adds lazy `request.json` attribute and serializes raw responses such as
`dict` or `(data: dict, status: int)` into JSON.

### Request

- `request.json` - parsed json
- `request.query` - parsed query (only after `@validate_query`)


### Response
You can just return `dict` of your date or you can add a status code

```python
def json_data(request):
    return {'hello': 'world'}

def with_status(request):
    return {'message': 'bad request'}, 400
```


### Auth
Decorators `@user_required` and `@staff_required` is analogous to
`login_required` and  `@staff_member_required` with JSON output instead of
redirecting

```python
from raw_api import staff_required

@staff_required
async def hello(request):
    return {'admin': 'zone'}
```


Data validation
---------------
You can use `@validate_query` and `@validate_json` decorators
to validate requests data. They're using [trafaret][] library to perform
validation.

```python
from raw_api import validate_json, validate_query

@validate_json({'ids': [int], 'hello?': str})
async def foo(request):
    return request.json

@validate_query({'id': int})
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
    python -m pytest tests/
```

[trafaret]: https://github.com/Deepwalker/trafaret
