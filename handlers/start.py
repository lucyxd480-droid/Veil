from pyrogram import filters
from core.state import games
from utils.keyboards import join_kb
from config import JOIN_TIME
import asyncio




def register_start(app):
@app.on_message(filters.command("startgame") & filters.group)
async def start(_, msg):
chat = msg.chat.id
games[chat].clear()
games[chat]["players"] = {}
games[chat]["phase"] = "join"


await msg.reply(
"🕯 THE VEIL OPENS...\nJoin within 60 seconds.",
reply_markup=join_kb()
)
