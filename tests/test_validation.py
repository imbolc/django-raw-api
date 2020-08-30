from django.test import Client


def test_query_empty():
    resp = Client().get("/query-validation")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "is required"},
    }


def test_async_query_empty():
    resp = Client().get("/async/query-validation")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "is required"},
    }


def test_query_wrong_type():
    resp = Client().get("/query-validation?id=foo")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "value can't be converted to int"},
    }


def test_async_query_wrong_type():
    resp = Client().get("/async/query-validation?id=foo")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "value can't be converted to int"},
    }


def test_query_extra_params():
    resp = Client().get("/query-validation?id=1&foo=bar")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"foo": "foo is not allowed key"},
    }


def test_async_query_extra_params():
    resp = Client().get("/async/query-validation?id=1&foo=bar")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"foo": "foo is not allowed key"},
    }


def test_query_ok():
    resp = Client().get("/query-validation?id=1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1}


def test_async_query_ok():
    resp = Client().get("/async/query-validation?id=1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1}


def test_json_method_not_allowed():
    resp = Client().get("/json-validation")
    assert resp.status_code == 405
    assert resp.json() == {"message": "Method not allowed"}


def test_async_json_method_not_allowed():
    resp = Client().get("/async/json-validation")
    assert resp.status_code == 405
    assert resp.json() == {"message": "Method not allowed"}


def test_json_empty():
    resp = Client().post("/json-validation", content_type="application/json")
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "is required"},
    }


def test_async_json_empty():
    resp = Client().post(
        "/async/json-validation", content_type="application/json"
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "is required"},
    }


def test_json_wrong_type():
    resp = Client().post(
        "/json-validation", {"id": "foo"}, content_type="application/json"
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "value can't be converted to int"},
    }


def test_async_json_wrong_type():
    resp = Client().post(
        "/async/json-validation",
        {"id": "foo"},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"id": "value can't be converted to int"},
    }


def test_json_extra_params():
    resp = Client().post(
        "/json-validation",
        {"id": 1, "foo": 2},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"foo": "foo is not allowed key"},
    }


def test_async_json_extra_params():
    resp = Client().post(
        "/async/json-validation",
        {"id": 1, "foo": 2},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "message": "Bad request",
        "errors": {"foo": "foo is not allowed key"},
    }


def test_json_ok():
    resp = Client().post(
        "/json-validation", {"id": "1"}, content_type="application/json"
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": 1}


def test_async_json_ok():
    resp = Client().post(
        "/async/json-validation", {"id": "1"}, content_type="application/json"
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": 1}
