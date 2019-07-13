=================
tamtam.py
=================

TamTam.py is about performance, so it requires ujson for serialization and deserialization, pydantic for models management, aiohttp for web requests


::

    pip install https://github.com/uwinx/tamtam.py.git


**Settings Bot-Info:**


.. code:: python

    from tamtam import Bot
    from tamtam.types.user import BotInfoSetter

    bot = Bot("put token @PrimeBot gave")

    async def func():
        info = BotInfoSetter(
            name="MyBotsName",
            description="smth...",
        )

        # There are two ways to SET:
        # 1 (beautiful):

        await info.call()

        # 2 (awful(comparing with first))
        await bot.set_me(info)

    asyncio.run(func())


=======================
Bots using tamtam.py
=======================

`GetJson
<https://tt.me/getjson>`_  this bot returns sent message's json (useful for developers or no)
