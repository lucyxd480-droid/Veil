import asyncio
import time
from pyrogram import filters

from core.state import game


def register_join(app):
    """
    Registers /join command and starts join timer
    """

    @app.on_message(filters.command("join"))
    async def join_handler(client, message):
        chat_id = message.chat.id
        user = message.from_user

        if not game.join_open:
            await message.reply("👐🏻 Joining is closed.")
            return

        if user.id in game.players:
            await message.reply("😈 You already joined.")
            return

        # first join → set chat_id
        if game.chat_id is None:
            game.chat_id = chat_id
            asyncio.create_task(monitor_join_time(app))

        game.players[user.id] = user.first_name

        await message.reply(
            f"✅ {user.first_name} joined the game!\n"
            f"👥 Total players: {len(game.players)}"
        )


async def monitor_join_time(app):
    """
    Monitors join timer and extends / closes joining
    """

    while game.join_open:
        remaining = int(game.join_end_time - time.time())

        if remaining <= 0:
            # extend join time ONCE if players < 5 (example)
            if not game.extended and len(game.players) < 5:
                game.extended = True
                game.join_end_time = time.time() + game.extend_duration

                await app.send_message(
                    game.chat_id,
                    "⏳ **Joining time extended!**\n"
                    "**15 seconds more to join** 👀"
                )

            else:
                game.join_open = False

                await app.send_message(
                    game.chat_id,
                    f"🔒 **Joining closed!**\n"
                    f"👥 Players joined: {len(game.players)}"
                )
                break

        await asyncio.sleep(1)
