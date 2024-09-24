import json
from typing import Any, Awaitable, Callable
from math_functions import *
from error_handler import *

# async def app(scope:dict[str, Any], receive:Callable[[], Awaitable[dict[str, Any]]], send: Callable[[dict[str, Any]], Awaitable[None]]):
#    ...
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
#    TODO: rename
   query_string = scope["query_string"].decode()
   params = dict(param.split("=") for param in query_string.split("&") if "=" in param)
   p_ =  scope['path'].split('/')[-1]

   if "n" not in params:
      
    await unprocessable_entity(send)
    try:
        num = int(p_)
        if num < 0:
            await bad_request(send)
            return
    except ValueError:
        await unprocessable_entity(send)
        return
    fibbonacci_value = fibbonacci_f(num)
    response = {"result":fibbonacci_value}
    await send_response(send, response)

async def handle_factorial(scope, receive, send):
   #    TODO: rename
#    query_string = scope.get('query_string', b''), 'n'
   query_string = scope["query_string"].decode('utf-8')
   params = dict(param.split("=") for param in query_string.split("&") if "=" in param)
#    p_ =  scope['path'].split('/')[-1]
   if "n" not in params:
      
    await unprocessable_entity(send)
    try:
        num = int(params["n"])
        if num < 0:
            await bad_request(send)
            return
    except ValueError:
        await unprocessable_entity(send)
        return
    factorial_value = factorial_f(num)
    response = {"result": factorial_value}
    await send_response(send, response) 
   

async def handle_mean(scope, receive, send):
#    query_string = scope.get('query_string', b'').decode('utf-8')
    body = await get_request_body(receive)
    try:
        numbers = json.loads(body)

        if not isinstance(numbers, list) or not all(
            isinstance(x, (int, float)) for x in numbers
        ):
            await unprocessable_entity(send)
            return

        if len(numbers) == 0:
            await bad_request(send)
            return

        mean_value = mean_f(numbers)
        response = {"result": mean_value}

        await send_response(send, response)

    except json.JSONDecodeError:
        await unprocessable_entity(send)


async def send_response(send, status_code, response_data):
    response_body = json.dumps(response_data).encode('utf-8')
    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })


async def get_request_body(receive):
    body = b""
    while True:
        message = await receive()
        if message['type'] == 'http.request':
            body += message.get('body', b'')
            if not message.get('more_body'):
                break
    return json.loads(body) if body else None