from tamtam import Bot, run_async
from tamtam.types import BotInfoSetter

Bot("token")


async def func():
    await BotInfoSetter(
        name="NewName", username="new_username", description="MyBot'NewDescription"
    ).call()


run_async(func())
