import asyncio
from typing import Callable, Any


async def wait(seconds: int, callback: Callable, *args: Any, **kwargs: Any):
    """
    Wait for `seconds` and then execute `callback`.

    Supports arguments and safe cancellation.
    """
    try:
        await asyncio.sleep(seconds)
        await callback(*args, **kwargs)
    except asyncio.CancelledError:
        # Task was cancelled intentionally (e.g., game ended)
        pass
    except Exception as e:
        print(f"[Timer Error] {e}")
