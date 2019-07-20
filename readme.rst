=================
👮‍♂️ tamtam.py
=================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: tamtam.py-code-style

.. image:: https://img.shields.io/badge/Python%203.7-blue.svg
    :target: https://www.python.org/
    :alt: tamtam.py-python-version

**💥 TamTam.py is about performance, so it requires ujson for serialization and deserialization, pydantic for models management, aiohttp for web requests**


::

    pip install https://github.com/uwinx/tamtam.py/archive/master.zip


**ℹ️ Setting bot-info:**


.. code:: python

    from tamtam import Bot, types, run_async

    Bot("put token @PrimeBot gave")

    async def func():
        info = await types.BotInfoSetter(
            name="MyBotsName",
            description="smth...",
        ).call()
        ...

    run_async(func())


--------------------------------
☂️ Write fancy decorators
--------------------------------

.. code:: python

    from tamtam import Dispatcher, Bot, run_poller, types

    dp = Dispatcher(Bot('token'))

    @dp.bot_started()
    async def start_handler(upd: types.BotStarted):
        await upd.respond("you started bot")

    run_poller()


---------------------------------------------------
👟 ⇒ 👞 Easily switch from polling to webhook
---------------------------------------------------

.. code:: python

    from tamtam import Bot, Dispatcher, types, run_sever

    bot = Bot("token")
    dp = Dispatcher(bot)

    @dp.bot_started()
    async def handler(upd: types.BotStarted):
        await upd.respond("Sup!")

    run_server()


-----------------------
If not configured:
-----------------------

.. code:: python

    # better example in repo/examples/
    async def sub(url):
        if not (await bot.subscribe(url))["success"]:
            # something went wrong
            ...
        ...

    url = "https://my.domain/path"  # or use yarl.URL.build

    from tamtam import run_async
    run_async(sub(url))


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

See `examples
<https://github.com/uwinx/tamtam.py/tree/master/examples>`_ for more.

=========================
Some advices from author
=========================

- Don't use webhooks. tamtam.py provides fantastically easy-to-use webhooks with no additional headaches, but also provides polling. You can use webhooks if you have special-cases. Cases like when you want to server multiple bots and etc. But for single bot(even high-loaded) you can use polling
- Avoid using low-level methods. If you are not super-smart and care consequences DO NOT use low-level methods. tamtam.py provides pretty enough user-friendly functions
- Don't use shitty libraries written with no love
- async/await syntax is easy. Asynchronous python won't bite you(if you code correctly)


==============
TODOs #help
==============

- Chats methods
- Easy creation of a message-attachment
