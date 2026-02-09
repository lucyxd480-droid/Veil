import asyncio
import time

from core.state import game
from utils.keyboards import join_keyboard

async def join_timer(app):
    me = await app.get_me()

    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining == 15 and 15 not in game.join_reminders_sent:
            game.join_reminders_sent.add(15)
            await app.send_message(
                game.chat_id,
                "⏳ **15 seconds left to join!**",
                reply_markup=join_keyboard(me.username)
            )

        if remaining <= 0:
            game.join_open = False

            if len(game.players) < 3:
                await app.send_message(
                    game.chat_id,
                    "🕯 Not enough players, cancelling game!"
                )
                game.reset()
                return

            game.phase = "ready"
            await app.send_message(
                game.chat_id,
                f"🔒 Joining closed! Players joined: {len(game.players)}\n"
                "Host can now start with /begin"
            )
            return

        await asyncio.sleep(1)
