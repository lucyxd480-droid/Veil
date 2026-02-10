from pyrogram import filters
from core.narrator import whisper


def register_horror(app):

    @app.on_message(filters.command("horror") & filters.group)
    async def horror_handler(client, message):
        line = whisper()
        await message.reply_text(f"🕯️ {line}")
