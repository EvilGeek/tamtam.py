from tamtam import Bot, Dispatcher, run_poller
from tamtam.types import Message, BotStarted
from tamtam.dispatcher.filters import MessageFilters

bot = Bot("put your token")
disp = Dispatcher(bot)


@disp.bot_started()
async def new_user(upd: BotStarted):
    await upd.respond(
        f"Hiya, {upd.user.name}, how're your doing?! Send me /start first"
    )


@disp.message_handler(MessageFilters.commands("start", "help"))
async def std_start(message: Message):
    await message.respond(f"{message.sender.name} send me anything")


@disp.message_handler()
async def any_msg(message: Message):
    await message.reply(message.json(indent=4))


run_poller()
