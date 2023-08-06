""" Contains functionality for working with asyncio """
import asyncio

import uvloop


class AsyncContext:
    """ Helper class which installs uvloop to the asyncio event loop """

    _loop = None

    @classmethod
    def get_loop(cls) -> asyncio.AbstractEventLoop:
        """
        Get the event loop. This class method always returns the same event loop,
        realizing a singleton pattern, to avoid conflicting event loop objects. It
        also installs uvloop to the event loop instance to maximize performance.
        """
        if cls._loop is None:
            uvloop.install()
            cls._loop = asyncio.get_event_loop()
        return cls._loop

    @classmethod
    def run(cls, async_fn) -> None:
        """
        Run async code in the uvloop-patched event loop.

        :param async_fn: The awaitable function/method to run
        """
        cls.get_loop().run_until_complete(async_fn)
