import asyncio, time
from core.state import game

async def join_timer(app):
    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining in (15, 10, 5):
            await app.send_message(
                game.chat_id,
                f"⏳ {remaining} seconds left to join!"
            )

        if remaining <= 0:
            if len(game.players) < 3:
                game.join_open = False
                game.phase = "idle"
                await app.send_message(
                    game.chat_id,
                    "🕯 Not enough players. Cancelling game..."
                )
                return

            game.join_open = False
            game.phase = "ready"
            await app.send_message(
                game.chat_id,
                f"🔒 Joining closed! {len(game.players)} players joined.\n"
                f"Admin can now begin the game with /begin"
            )
            return

        await asyncio.sleep(1)
