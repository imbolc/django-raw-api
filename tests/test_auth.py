import pytest
from django.contrib.auth import get_user_model
from django.test import Client


def test_user_guest():
    c = Client()
    resp = c.get("/require-user")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


def test_async_user_guest():
    c = Client()
    resp = c.get("/async/require-user")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_user_inactive():
    c = Client()
    user = get_user_model().objects.get_or_create(
        username="inactive_user", email="inactive@user.com"
    )[0]
    c.force_login(user)
    user.is_active = False
    user.save()
    resp = c.get("/require-user")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_async_user_inactive():
    c = Client()
    user = get_user_model().objects.get_or_create(
        username="inactive_user", email="inactive@user.com"
    )[0]
    c.force_login(user)
    user.is_active = False
    user.save()
    resp = c.get("/async/require-user")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_user_success():
    user = get_user_model().objects.get_or_create(
        username="user", email="some@user.com"
    )[0]
    c = Client()
    c.force_login(user)
    resp = c.get("/require-user")
    assert resp.status_code == 200
    assert resp.json() == {"user": "user"}


@pytest.mark.django_db(transaction=True)
def test_async_user_success():
    user = get_user_model().objects.get_or_create(
        username="user", email="some@user.com"
    )[0]
    c = Client()
    c.force_login(user)
    resp = c.get("/async/require-user")
    assert resp.status_code == 200
    assert resp.json() == {"user": "user"}


def test_staff_guest():
    c = Client()
    resp = c.get("/require-staff")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


def test_async_staff_guest():
    c = Client()
    resp = c.get("/async/require-staff")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_staff_inactive():
    user = get_user_model().objects.get_or_create(
        username="inactive_staff", email="inactive@staff.com", is_staff=True
    )[0]
    c = Client()
    c.force_login(user)
    user.is_active = False
    user.save()
    resp = c.get("/require-staff")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_async_staff_inactive():
    user = get_user_model().objects.get_or_create(
        username="inactive_staff", email="inactive@staff.com", is_staff=True
    )[0]
    c = Client()
    c.force_login(user)
    user.is_active = False
    user.save()
    resp = c.get("/async/require-staff")
    assert resp.status_code == 403
    assert resp.json() == {"message": "You have to log in"}


@pytest.mark.django_db
def test_staff_success():
    user = get_user_model().objects.get_or_create(
        username="staff", email="some@staff.com", is_staff=True
    )[0]
    c = Client()
    c.force_login(user)
    resp = c.get("/require-staff")
    assert resp.status_code == 200
    assert resp.json() == {"user": "staff"}


@pytest.mark.django_db(transaction=True)
def test_async_staff_success():
    user = get_user_model().objects.get_or_create(
        username="staff", email="some@staff.com", is_staff=True
    )[0]
    c = Client()
    c.force_login(user)
    resp = c.get("/async/require-staff")
    assert resp.status_code == 200
    assert resp.json() == {"user": "staff"}
