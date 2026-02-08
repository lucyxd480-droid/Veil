from pyrogram import filters
from core.state import game
from utils.keyboards import join_keyboard
from utils.text import START_TEXT
from handlers.join_timer import start_join_timer
import asyncio


def register_start(app):

    @app.on_message(filters.group & filters.command("start"))
    async def start_group(client, message):
        if game.join_open:
            await message.reply("🕯 A game is already forming.")
            return

        game.reset()
        game.join_open = True

        await message.reply(
            START_TEXT,
            reply_markup=join_keyboard()
        )

        asyncio.create_task(
            start_join_timer(app, message.chat.id)
        )
