from pyrogram import filters
from core.engine import GAMES, run_game
from core.state import GameState
import asyncio

def register_admin(app):

    @app.on_message(filters.command("startgame") & filters.group)
    async def start(_, msg):
        chat_id = msg.chat.id
        if chat_id in GAMES:
            return

        state = GameState(chat_id)
        GAMES[chat_id] = state
        asyncio.create_task(run_game(app, state))
        await msg.reply("The Veil has opened.")
