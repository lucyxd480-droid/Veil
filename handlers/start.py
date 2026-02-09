import asyncio
import time

from pyrogram import filters
from core.state import game
from handlers.join_timer import join_timer
from utils.keyboards import join_keyboard
from utils.text import START_TEXT

def register_start(app):

    @app.on_message(filters.group & filters.command("startgame"))
    async def start_game(_, msg):
        if game.join_open or game.phase in {"ready", "round", "voting"}:
            return await msg.reply("🕯 A game is already active in this group.")

        game.reset()
        game.join_open = True
        game.chat_id = msg.chat.id
        game.host_id = msg.from_user.id if msg.from_user else None
        game.host_name = msg.from_user.first_name if msg.from_user else "Unknown"
        game.phase = "join"
        game.join_duration = 60
        game.join_end_time = time.time() + game.join_duration

        me = await app.get_me()
        await msg.reply(
            START_TEXT.format(host=game.host_name),
            reply_markup=join_keyboard(me.username)
        )

        asyncio.create_task(join_timer(app))
