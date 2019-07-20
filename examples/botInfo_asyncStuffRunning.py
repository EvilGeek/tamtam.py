from tamtam import Bot, run_async, types

Bot("TOKEN")


async def func() -> types.User:
    return await types.BotInfoSetter(
        name="BotNewName",
        username="new_username",
        description="https://github.com/uwinx/tamtam.py powered bot!",
    ).call()


# just a way to run async functions
for i in run_async(func(), func()):
    print(i)
