from pyrogram import filters

from core.flow import schedule_join_expiry
from core.state import games
from utils.auth import ensure_admin


def register_extend(app):
    @app.on_message(filters.command("extend") & filters.group)
    async def extend(client, msg):
        # Admin permission check
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or game.get("phase") != "join":
            return await msg.reply("❌ No active join timer.")

        if len(msg.command) < 2:
            return await msg.reply("Usage: /extend 30")

        try:
            extra = int(msg.command[1])
        except ValueError:
            return await msg.reply("Usage: /extend 30")

        # Prevent abuse (negative or insane numbers)
        extra = max(1, extra)

        game["join_seconds"] += extra

        # Reset timer with new duration
        await schedule_join_expiry(app, chat_id, game["join_seconds"])

        await msg.reply(
            f"⏳ Join timer reset and extended to {game['join_seconds']} seconds."
        )
