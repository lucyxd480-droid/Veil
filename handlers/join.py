import asyncio
import time
from pyrogram import filters
from core.state import game

MIN_PLAYERS = 6


def register_join(app):

    @app.on_message(filters.command("join"))
    async def join_handler(client, message):
        user = message.from_user
        chat_id = message.chat.id

        if not game.join_open:
            await message.reply("👐🏻 Joining is closed.")
            return

        if user.id in game.players:
            await message.reply("😈 You already joined.")
            return

        if game.chat_id is None:
            game.chat_id = chat_id
            asyncio.create_task(monitor_join_time(app))

        game.players[user.id] = user.first_name

        await message.reply(
            f"✅ {user.first_name} joined!\n"
            f"👥 Players: {len(game.players)}/{MIN_PLAYERS}"
        )


async def monitor_join_time(app):

    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining <= 0:
            game.join_open = False

            await app.send_message(
                game.chat_id,
                f"🔒 **Joining closed!**\n"
                f"👥 Players: {len(game.players)}\n\n"
                f"▶️ Use /start to begin the game"
            )
            break

        await asyncio.sleep(1)
