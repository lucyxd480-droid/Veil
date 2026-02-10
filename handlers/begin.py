from pyrogram import filters
from core.state import games, GameState
from utils.texts import INTRO
from utils.keyboards import join_kb

def register_begin(app):
    @app.on_message(filters.command("begin") & filters.group)
    async def begin(_, msg):
        chat_id = msg.chat.id
        if chat_id in games and games[chat_id].active:
            return await msg.reply("Game already running.")

        game = GameState(chat_id)
        game.active = True
        games[chat_id] = game

        await msg.reply(INTRO, reply_markup=join_kb())
