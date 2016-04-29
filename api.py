import aiohttp
from aiohttp import web
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_token(token):
    if token == "demo123":
        return True, "OK"
    else:
        return False, "FAIL"


def load_score(title):
    return True, "60%"


def handle_error(ws):
    logger.exception("ws connection closed with exception {0}".format(ws.exception()))


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    pipeline = iter([validate_token, load_score])

    async for msg in ws:
        cmd = next(pipeline)
        if msg.tp == aiohttp.MsgType.text:
            if msg == "close":
                await ws.close()
            else:
                result, msg = cmd(msg.data)
                ws.send_str(msg)
                if not result:
                    await ws.close()
                    break

        elif msg.tp == aiohttp.MsgType.error:
            handle_error(ws)

    return ws

api = web.Application()

api.router.add_route("GET", "/", ws_handler)
