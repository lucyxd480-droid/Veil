from pyrogram import filters
from core.state import games
from core.engine import assign_roles
from utils.keyboards import join_kb

def register_start(app):
    @app.on_message(filters.command("startgame") & filters.group)
    async def start(_, msg):
        chat = msg.chat.id

        games[chat].clear()
        games[chat]["players"] = {}
        games[chat]["roles"] = {}
        games[chat]["alive"] = set()
        games[chat]["phase"] = "join"

        await msg.reply(
            "🕯 THE VEIL OPENS...\nJoin within 60 seconds.",
            reply_markup=join_kb()
        )
