import asyncio


async def wait(seconds, callback):
    await asyncio.sleep(seconds)
    await callback()
