from pyrogram import filters
from core.engine import GAMES, run_game
from core.state import GameState
from utils.keyboards import join_keyboard
import asyncio

def register_admin(app):

    @app.on_message(filters.command("startgame") & filters.group)
    async def start(_, msg):
        chat_id = msg.chat.id

        if chat_id in GAMES:
            await msg.reply("🎃 A game is already running.")
            return

        state = GameState(chat_id)
        GAMES[chat_id] = state

        await msg.reply(
            "🎃 **Game Started!**\n"
            "⏳ **30 seconds to join**",
            reply_markup=join_keyboard()
        )

        asyncio.create_task(run_game(app, state))
