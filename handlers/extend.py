from pyrogram import filters
from core.flow import schedule_join_expiry
from core.state import games


def register_extend(app):
    @app.on_message(filters.command("extend") & filters.group)
    async def extend(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game or game.get("phase") != "join":
            return await msg.reply("❌ No active join timer.")

        try:
            extra = int(msg.command[1])
        except Exception:
            return await msg.reply("Usage: /extend 30")

        # Extend join time and reschedule
        game["join_seconds"] += max(1, extra)
        await schedule_join_expiry(app, chat, game["join_seconds"])
        await msg.reply(f"⏳ Join timer reset and extended to {game['join_seconds']} seconds.")
