from pyrogram import filters
import asyncio

from core.state import game
from utils.keyboards import join_keyboard
from utils.text import START_TEXT
from handlers.join_timer import start_join_timer


def register_start(app):

    @app.on_message(filters.group & filters.command("start"))
    async def start_group(_, msg):
        if game.join_open:
            await msg.reply("🕯 A game is already forming.")
            return

        game.reset()
        game.join_open = True
        game.chat_id = msg.chat.id

        await msg.reply(
            START_TEXT,
            reply_markup=join_keyboard()
        )

        asyncio.create_task(
            start_join_timer(app, msg.chat.id)
        )
