import asyncio
import uuid

from django.shortcuts import render

from raw_api import (
    staff_required,
    user_required,
    validate_json,
    validate_query,
)

SLEEP = 1


def index(request):
    return render(request, "index.html", {"sleep": SLEEP})


@staff_required
@validate_query({"id": int})
async def query(request):
    await sleep()
    return request.query


@validate_json({"id": int})
async def json(request):
    await sleep()
    return request.json


@user_required
async def user(request):
    await sleep()
    return request.user.username


@staff_required
async def staff(request):
    await sleep()
    return request.user.username


async def sleep():
    request_id = str(uuid.uuid4())
    print(f"{request_id=} fall asleep")
    await asyncio.sleep(SLEEP)
    print(f"{request_id=} woke up")
