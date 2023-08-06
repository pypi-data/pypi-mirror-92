"""Common async functions."""

import asyncio
import signal
import zlib
from asyncio import AbstractEventLoop, Future, Task
from functools import partial
from typing import Optional, Sequence, Set


async def stop(tasks: Sequence[Task], loop: AbstractEventLoop) -> None:
    """Stop tasks."""

    for task in tasks:
        task.cancel()

    pending: Set[Future] = {*tasks}

    while pending:
        _, pending = await asyncio.wait(pending)

    loop.stop()


def register_stop(tasks: Sequence[Task], loop: AbstractEventLoop) -> None:
    """Register stop handler."""

    loop.add_signal_handler(signal.SIGINT, partial(asyncio.ensure_future, stop(tasks, loop)))


def wrap(data: bytes, topic: Optional[str] = None, compress: bool = False) -> bytes:
    """Wrap data with compression and topic prefix."""

    if compress:
        data = zlib.compress(data)

    return f"{topic}|".encode("utf-8") + data


def peel(data: bytes, topic: Optional[str] = None, compress: bool = False) -> bytes:
    """Unwrap data removing topic and compression."""

    try:
        _, data = data.split(b"|", 1)
    except ValueError:
        raise ValueError("Missing topic on data")

    if compress:
        data = zlib.decompress(data)

    return data
