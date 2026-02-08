from pyrogram import filters
from core.state import game
from utils.keyboards import join_keyboard
from utils.text import START_TEXT
from handlers.join_timer import join_timer
import asyncio, time

def register_start(app):

    @app.on_message(filters.group & filters.command("startgame"))
    async def start_game(_, msg):
        if game.join_open:
            return await msg.reply("🕯 A game is already forming!")

        game.reset()
        game.join_open = True
        game.chat_id = msg.chat.id
        game.phase = "join"
        game.join_duration = 60
        game.join_end_time = time.time() + game.join_duration

        await msg.reply(
            f"✨ **A new Veil game has been started by {msg.from_user.first_name}!**\n"
            f"🎯 Come join and prove your presence!\n\n"
            f"#Players: 0\n\n"
            f"Click Join below to enter!",
            reply_markup=join_keyboard()
        )

        asyncio.create_task(join_timer(app))
