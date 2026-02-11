from pyrogram import filters

from core.narrator import whisper
from core.state import games, new_game_state
from utils.auth import ensure_admin


def register_end(app):
    @app.on_message(filters.command("endgame") & filters.group)
    async def end(client, msg):
        # Admin check
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game:
            return await msg.reply("❌ No active game to end.")

        # Cancel running tasks safely
        for task_key in ("join_task", "phase_task"):
            task = game.get(task_key)
            if task and not task.done():
                task.cancel()

        # Reset state
        games[chat_id] = new_game_state()

        await msg.reply(
            f"🕯 THE VEIL FALLS.\n{whisper()}"
        )
