import json


async def bad_request(send):
    await send(
        {
            "type": "http.response.start",
            "status": 400,
            "headers": [(b"content-type", b"application/json")],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "400 Bad Request"}).encode("utf-8"),
        }
    )


async def not_found(send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "404 Not Found"}).encode("utf-8"),
        }
    )


async def unprocessable_entity(send):
    await send(
        {
            "type": "http.response.start",
            "status": 422,
            "headers": [(b"content-type", b"application/json")],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "422 Unprocessable Entity"}).encode("utf-8"),
        }
    )
