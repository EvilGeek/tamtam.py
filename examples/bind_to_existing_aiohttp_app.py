import asyncio
import logging

from aiohttp import web
from tamtam import run_server, Bot, Dispatcher, types, filters

PRIV_TOKEN = "token"
ME = 123456789

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(PRIV_TOKEN)
dp = Dispatcher(bot)
app = web.Application()


def get_ip(request: web.Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for

    peer_name = request.transport.get_extra_info("peername")

    if peer_name is not None:
        return peer_name


async def base_handler(request: web.Request) -> web.Response:
    message = await bot.send_message(
        types.NewMessage(text=f"Site was visited by {get_ip(request)}"), user_id=ME
    )

    return web.json_response({"ok": True if message else False})


@dp.message_handler(filters.MessageFilters.exact("(82.crmvl32&271"))
async def secret_message_handler(message: types.Message):
    await message.reply(text="Hello, comrade mayor!")


# webhooks configurations you can run it once that wil be enough
async def configure_webhooks():
    import yarl
    import hashlib

    scheme = "http"
    host = "1o1l0l.ngrok.io"
    path = hashlib.blake2b(PRIV_TOKEN.encode(), digest_size=32).hexdigest()
    port = 25000

    base_url = yarl.URL.build(scheme=scheme, host=host)
    url = base_url.with_path(path).with_port(port)

    # unsubscribe all existing urls [Optional]
    [await bot.unsubscribe(sub.url) for sub in await bot.subscriptions()]

    await bot.subscribe(types.NewSubscriptionConfig(url=str(url)))

    configurations = {"host": url.host, "port": url.port, "path": url.path}

    print(configurations)

    return configurations


app.router.add_get("/", base_handler, name="base-hello-router-1")
run_server(app=app, **loop.run_until_complete(configure_webhooks()))
