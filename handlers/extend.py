from pyrogram import filters
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
        except:
            return await msg.reply("Usage: /extend 30")

        await msg.reply(f"⏳ Join time extended by {extra} seconds.")
