import asyncio
import typing

from aiohttp import client_exceptions

from . import Dispatcher

loop = asyncio.get_event_loop()


def run_async(*coroutines, tasks=False):
    if coroutines:
        for coro in coroutines:
            if tasks:
                loop.create_task(coro)
            else:
                yield loop.run_until_complete(coro)


def run_poller(
    *coroutines,
    lim: int = 100,
    marker: int = -1,
    timeout: typing.Union[float, int] = 30,
    update_types: typing.Optional[str] = None,
    exit_on_exc: typing.Sequence = (KeyboardInterrupt,),
    on_exc_callback: typing.Callable[..., typing.NoReturn] = lambda: print("Bye :*"),
    sleep_after_call: typing.Union[float, int] = 0.1,
):
    """
    Function to idle dispatcher synchronously in event loop [This is blocking function]

        *coroutines - Pass coroutines you want run and FORGET(!) BEFORE idling starts

    :param lim int [1..1000] default is 100 Maximum number of updates to be retrieved
    :param timeout int [0..90] default is 30 Timeout in seconds for long polling
    :param marker int Nullable Pass null to get updates you didn't get yet 
    :param update_types str array of joint string update types example "types=message_created,message_callback"
    :param exit_on_exc Exception
    :param on_exc_callback on_app_close primitive sync callback
    :param sleep_after_call sleep seconds after each call
    """
    try:
        dispatcher = Dispatcher.current()

        assert dispatcher, "Dispatcher was never initialized"

        run_async(coroutines, tasks=True)

        loop.run_until_complete(
            dispatcher.poll(
                lim=lim,
                marker=marker,
                timeout=timeout,
                update_types=update_types,
                sleep_after_call=sleep_after_call,
            )
        )

    except exit_on_exc:
        if on_exc_callback:
            on_exc_callback()

        loop.close()  # exit case

    except (client_exceptions.ClientError,):
        loop.close()  # exit case


def run_server(*coroutines, host: str, port: int, path: str, app=None):
    run_async(coroutines, tasks=True)

    dispatcher = Dispatcher.current()
    assert dispatcher, "Dispatcher was never initialized"

    dispatcher.listen(host=host, port=port, path=path, app=app)
