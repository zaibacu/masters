import aiohttp
from aiohttp import web
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def validate_token(token):
    if token == "demo123":
        return True, "OK"
    else:
        return False, "FAIL"


async def load_score(title):
    import asyncio
    from rank.util import purge
    from rank.collect.movie import get_comments
    loop = asyncio.get_event_loop()
    data = get_comments(title.strip())
    lines = ["| {0}".format(purge(comment)) for comment in data]

    logger.debug("Got comments")
    create = asyncio.create_subprocess_exec("vw", "-c", "-k", "-t", "-i", "data/raw.vw", "-p", "/dev/stdout", "--quiet",
                                            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)

    logger.debug("Creating classifier")
    proc = await create
    proc.stdin.write("\n".join(lines).encode("UTF-8"))
    await proc.stdin.drain()
    proc.stdin.close()
    result = await proc.stdout.read()
    await proc.wait()

    from score import score, parse_num

    logger.debug("Calculating score")
    ratings = [parse_num(line) for line in result.decode("UTF-8").split("\n")]
    for r, c in zip(ratings, data):
        logger.debug("Rating: {0}, Comment: {1}".format(r, c))
    mean = score(ratings[:-1], base=10)
    return True, str(mean)


def handle_error(ws):
    logger.exception("ws connection closed with exception {0}".format(ws.exception()))


async def ws_handler(request):
    ws = web.WebSocketResponse(timeout=60)
    await ws.prepare(request)

    pipeline = iter([validate_token, load_score])

    async for msg in ws:
        cmd = next(pipeline)
        if msg.tp == aiohttp.MsgType.text:
            if msg == "close":
                await ws.close()
            else:
                result, msg = await cmd(msg.data)
                ws.send_str(msg)
                if not result:
                    await ws.close()
                    break

        elif msg.tp == aiohttp.MsgType.error:
            handle_error(ws)

    return ws

api = web.Application()

api.router.add_route("GET", "/", ws_handler)
