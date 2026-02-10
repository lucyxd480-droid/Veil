from pyrogram import filters
from core.state import games




def register_discussion(app):
@app.on_message(filters.command("discuss") & filters.group)
async def discuss(_, msg):
chat = msg.chat.id
games[chat]["phase"] = "discussion"
await msg.reply("🧠 Discuss. Judgment comes soon.")
