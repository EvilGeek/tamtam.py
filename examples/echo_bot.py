from tamtam import Bot, Dispatcher, run_poller
from tamtam.types.updates import Message, BotStarted
from tamtam.dispatcher.filters import MessageFilters


bot = Bot("put token")
dp = Dispatcher(bot)


@dp.bot_started()
async def new_user(upd: BotStarted):
    await upd.respond(f"Hello! {upd.user.name}.\nNice to see you!")


@dp.message_handler(MessageFilters(commands=["start"]))
async def cmd_start(message: Message):
    await message.reply(f"Hey there, {message.sender.name}! This is echo-bot.")


@dp.message_handler()
async def echo(message: Message):
    await message.reply(message.body.text)


run_poller()
