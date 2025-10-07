# Trying to introduce async function for asynchronous beamline control
# Add by Siyu Wu 2025/08/21

import asyncio
import threading
import contextlib
import queue
from concurrent.futures import ThreadPoolExecutor

def async_run(func, *args, **kwargs):
    """
    Run a synchronous function in an asynchronous context.
    """
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError:
        try:
            import nest_asyncio
            nest_asyncio.apply()
        except Exception:
            pass
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, func, *args, **kwargs)

