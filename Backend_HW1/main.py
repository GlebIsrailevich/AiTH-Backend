import json

from error_handler import *
from math_functions import *


async def app(scope, receive, send) -> None:
    assert scope["type"] == "http"

    if scope["method"] == "GET" and scope["path"] == "/factorial":
        await handle_factorial(scope, receive, send)

    elif scope["method"] == "GET" and scope["path"].startswith("/fibonacci"):
        await handle_fibonacci(scope, receive, send)

    elif scope["method"] == "GET" and scope["path"] == "/mean":
        await handle_mean(scope, receive, send)

    else:
        await not_found(send)


async def handle_fibonacci(scope, receive, send):
    try:
        params_fib = scope["path"].split("/")[-1]
    except ValueError:
        await unprocessable_entity(send)
        return
    try:
        num = int(params_fib)
    except ValueError:
        await unprocessable_entity(send)
        return
    if num < 0:
        await bad_request(send)
        return
    fibbonacci_value = fibbonacci_f(num)
    response = {"result": fibbonacci_value}
    await send_response(send, 200, response)


async def handle_factorial(scope, receive, send):
    query_string = scope["query_string"].decode("utf-8")
    params_factorial = dict(
        param.split("=") for param in query_string.split("&") if "=" in param
    )
    if "n" not in params_factorial:
        await unprocessable_entity(send)
        return
    try:
        num = int(params_factorial["n"])
    except ValueError:
        await unprocessable_entity(send)
        return
    if num < 0:
        await bad_request(send)
        return
    factorial_value = factorial_f(num)
    response = {"result": factorial_value}
    await send_response(send, 200, response)


async def handle_mean(scope, receive, send):
    try:
        body = await get_request_body(receive)
    except ValueError:
        await unprocessable_entity(send)
        return
    try:
        numbers = json.loads(body)

        if not isinstance(numbers, list) or not all(
            isinstance(x, (int, float)) for x in numbers
        ):
            await unprocessable_entity(send)
            return

        if numbers is None:
            await unprocessable_entity(send)
            return

        if len(numbers) == 0:
            await bad_request(send)
            return

        mean_value = mean_f(numbers)
        response = {"result": mean_value}

        await send_response(send, 200, response)

    except json.JSONDecodeError:
        await unprocessable_entity(send)


async def send_response(send, status_code, response_data):
    response_body = json.dumps(response_data).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": response_body,
        }
    )


async def get_request_body(receive):
    body = b""
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    return body
