from pyrogram import filters
from core.state import games
from utils.keyboards import pick_kb




def register_pick(app):
@app.on_message(filters.command("pick") & filters.group)
async def pick(_, msg):
chat = msg.chat.id
game = games[chat]
players = list(game["players"].values())
await msg.reply("Choose the condemned:", reply_markup=pick_kb(players))
