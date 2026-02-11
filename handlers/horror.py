from pyrogram import filters
from core.horror import horror


def register_horror(app):
    @app.on_message(filters.command("horror") & filters.group)
    async def horror_cmd(_, msg):
        await msg.reply(f"🕯 {horror()}")
