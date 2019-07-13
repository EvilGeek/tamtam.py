from tamtam import Bot, Dispatcher, run_poller
from tamtam.types.messages import Message

bot = Bot("token")
disp = Dispatcher(bot)


@disp.message_handler(commands=["start", "help"])
async def std_start(message: Message):
    await message.respond(
        f"Hey there, {message.sender.name}! I'll show you any messages json"
    )


@disp.message_handler()
async def any_msg(message: Message):
    await message.reply(message.json(indent=4))


run_poller()
