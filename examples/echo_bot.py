from tamtam import Bot, Dispatcher, run_poller
from tamtam.types.messages import Message


bot = Bot("put your token here")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    await message.reply(f"Hey there, {message.sender.name}! This is echo-bot.")


@dp.message_handler()
async def echo(message: Message):
    await message.reply(message.body.text)


run_poller()
