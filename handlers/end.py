from pyrogram import filters
from core.state import games
from core.narrator import whisper


def register_end(app):
    @app.on_message(filters.command("endgame") & filters.group)
    async def end(_, msg):
        chat = msg.chat.id
        games.pop(chat, None)
        await msg.reply(f"🕯 THE VEIL FALLS.\n{whisper()}")
