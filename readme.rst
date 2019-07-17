=================
👮‍♂️ tamtam.py
=================

TamTam.py is about performance, so it requires ujson for serialization and deserialization, pydantic for models management, aiohttp for web requests


::

    pip install https://github.com/uwinx/tamtam.py/archive/master.zip


**Settings Bot-Info:**


.. code:: python

    from tamtam import Bot, types

    Bot("put token @PrimeBot gave")

    async def func():
        info = await types.BotInfoSetter(
            name="MyBotsName",
            description="smth...",
        ).call()

    asyncio.run(func())


------------------------
Write fancy decorators
------------------------

.. code:: python

    from tamtam import Dispatcher, Bot, run_poller, types

    dp = Dispatcher(Bot('token'))

    @dp.bot_started()
    async def start_handler(upd: types.BotStarted):
        await upd.respond("you started bot")

    run_poller()

--------------------------------------
Easily switch from polling to webhook
--------------------------------------


.. code::python

    from tamtam import Bot, Dispatcher, types
    from tamtam.runner import run_server, run_async

    bot = Bot("token")
    dp = Dispatcher(bot)

    @dp.bot_started()
    async def handler(upd: types.BotStarted):
        await upd.respond("Sup!")

    run_server()


**If not configured:**


.. code::python

    async def sub(url):
        if not (await bot.subscribe(url))["success"]:
            # something went wrong
            ...
        ...

    url = "https://my.domain/path"  # or use yarl.URL.build
    run_async(sub())


-------------------------------------
Easy function based message filters
-------------------------------------

.. code:: python

    from tamtam import Dispatcher, Bot, run_poller, types
    from tamtam.dispatcher.filters import MessageFilters

    dp = Dispatcher(Bot('token'))

    @dp.message_handler(MessageFilters.match(r"^.ban \d$"))
    async def ban_user_handler(message: types.Message):
        ...

=======================
Bots using tamtam.py
=======================

`GetJson
<https://tt.me/getjson>`_  this bot returns sent message's json (useful for developers or no)
