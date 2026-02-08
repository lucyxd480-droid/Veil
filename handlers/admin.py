from pyrogram import filters
from core.state import game


def register_admin(app):

    @app.on_message(filters.group & filters.command("extend"))
    async def extend(_, msg):
        if game.join_open:
            game.join_end_time += game.extend_duration
            await msg.reply("⏳ Joining time extended.")

    @app.on_message(filters.group & filters.command("cancel"))
    async def cancel(_, msg):
        game.reset()
        await msg.reply("🕯 The Veil has been closed.")
