from pyrogram import filters
from core.state import games
from utils.keyboards import enter_kb
from config import MIN_PLAYERS

def register_join(app):
    @app.on_callback_query(filters.regex("^join$"))
    async def join(_, cq):
        game = games.get(cq.message.chat.id)
        if not game:
            return

        uid = cq.from_user.id
        game.players[uid] = cq.from_user.first_name
        game.alive.add(uid)

        await cq.answer("Joined 🕯", show_alert=True)

        if len(game.players) == MIN_PLAYERS:
            await cq.message.reply("🕯 Darkness ready.", reply_markup=enter_kb())
