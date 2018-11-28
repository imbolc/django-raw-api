from django.test import Client


def test_dict_response():
    c = Client()
    resp = c.get("/dict")
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
    assert resp["content-type"] == "application/json"


def test_tuple_response():
    c = Client()
    resp = c.get("/tuple")
    assert resp.status_code == 400
    assert resp.json() == {"bad": "request"}


def test_django_response():
    c = Client()
    resp = c.get("/django-response")
    assert resp.status_code == 200
    assert resp.content == b"foo"


def test_empty_json_request():
    c = Client()
    resp = c.get("/request-json")
    assert resp.status_code == 400


def test_broken_json_request():
    c = Client()
    resp = c.post("/request-json", {"form": "data"})
    assert resp.status_code == 400


def test_correct_json_request():
    c = Client()
    resp = c.post("/request-json", {"foo": 1}, content_type="application/json")
    assert resp.status_code == 200
    assert resp.json() == {"foo": 1}
