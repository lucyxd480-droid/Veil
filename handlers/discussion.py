from pyrogram import filters

from core.flow import start_discussion
from core.state import games
from utils.auth import ensure_admin


def register_discussion(app):
    @app.on_message(filters.command("discuss") & filters.group)
    async def discuss(client, msg):
        # Admin permission check
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")

        # Optional: prevent triggering from wrong phase
        if game.get("phase") not in {"night", "discussion"}:
            return await msg.reply("❌ Cannot start discussion right now.")

        await start_discussion(app, chat_id)
        await msg.reply("🧠 Discussion manually started.")
