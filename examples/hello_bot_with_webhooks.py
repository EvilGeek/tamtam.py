from tamtam import Bot, Dispatcher, types
from tamtam.runner import run_server, run_async

TOKEN = "token"
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.bot_started()
async def new_pm_user(action: types.BotStarted):
    await action.respond("Add me to your channel!")


@dp.OnChatEvent.user_added()
async def new_user(action: types.UserAdded):
    await action.respond("Hello! :)")


@dp.OnChatEvent.user_removed()
async def user_removed(action: types.UserRemoved):
    await action.respond("We won't forget you! :c")


async def server_setup(url):
    info = await bot.subscribe(types.NewSubscriptionConfig(
        url=str(url),
    ))

    print(info["success"])


if __name__ == "__main__":
    # do it once:
    import yarl
    import hashlib

    scheme = "https"
    port = 8443
    base = "mysite.domain"
    path = hashlib.blake2b(TOKEN.encode(), digest_size=16).hexdigest()
    my_url = yarl.URL.build(scheme=scheme, host=base, port=port).with_path(path)

    run_async(server_setup(my_url))
    # till here

    run_server()
