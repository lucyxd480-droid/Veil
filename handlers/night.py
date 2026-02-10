from pyrogram import filters
from core.state import games
from core.narrator import whisper




def register_night(app):
@app.on_message(filters.command("night") & filters.group)
async def night(_, msg):
chat = msg.chat.id
games[chat]["phase"] = "night"
await msg.reply(f"🌑 Night falls...\n{whisper()}")
