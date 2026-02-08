import asyncio
import time
from core.state import game


async def start_join_timer(app, chat_id):
    game.join_end_time = time.time() + game.join_duration

    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining <= 0:
            if not game.extended:
                game.extended = True
                game.join_end_time = time.time() + game.extend_duration

                await app.send_message(
                    chat_id,
                    "⏳ **Joining time extended!**\n15 seconds more…"
                )
            else:
                game.join_open = False
                game.phase = "ready"

                await app.send_message(
                    chat_id,
                    "🔒 **Joining closed.**\nAdmin may begin the game."
                )
                break

        elif remaining in (15, 10, 5):
            await app.send_message(
                chat_id,
                f"⏳ {remaining} seconds left to join…"
            )

        await asyncio.sleep(1)
