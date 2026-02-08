import time
from pyrogram import filters
from core.state import game


def register_admin(app):

    @app.on_message(filters.command("extend"))
    async def extend_handler(client, message):

        if not game.join_open:
            await message.reply("❌ Joining is already closed.")
            return

        game.join_end_time += game.extend_duration

        await message.reply(
            f"⏳ **Joining extended by {game.extend_duration} seconds**"
        )

    @app.on_message(filters.command("cancel"))
    async def cancel_handler(client, message):

        game.cancel()

        await message.reply("🛑 **Game cancelled and reset.**")
