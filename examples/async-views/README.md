Async-view
==========

An django app using `raw-api` with async view introduced in django 3.1

Start it with: `uvicorn asgi:application`
Make async requests with: `time seq 1 5 | xargs -n1 -P5  curl http://localhost:8000/`
