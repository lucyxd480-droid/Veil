import asyncio
import time
from core.state import game

async def monitor_join_time(chat_id):
    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining <= 0:
            if not game.extended and len(game.players) >= 3:
                game.extended = True
                game.join_end_time = time.time() + game.extend_duration

                await app.send_message(
                    chat_id,
                    "⏳ **Joining time extended!**\n"
                    "**15 seconds more to join** 👀"
                )
            else:
                game.join_open = False
                await app.send_message(
                    chat_id,
                    f"🔒 **Joining closed!**\n"
                    f"👥 Players joined: {len(game.players)}"
                )
                break

        await asyncio.sleep(1)
