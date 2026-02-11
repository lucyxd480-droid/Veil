from pyrogram import filters
from core.narrator import whisper
from core.state import games, new_game_state


def register_end(app):
    @app.on_message(filters.command("endgame") & filters.group)
    async def end(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        # Cancel any running tasks
        if game:
            for key in ("join_task", "phase_task"):
                task = game.get(key)
                if task and not task.done():
                    task.cancel()

        # Reset the game state
        games[chat] = new_game_state()
        await msg.reply(f"🕯 THE VEIL FALLS.\n{whisper()}")
