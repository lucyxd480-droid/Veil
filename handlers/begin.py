from pyrogram import filters
import asyncio
from core.state import game
from utils.text import ROUND_DM_TEXT
from utils.keyboards import dm_options_keyboard


def register_begin(app):

    @app.on_message(filters.group & filters.command("begin"))
    async def begin_game(_, message):

        # basic checks
        if game.phase != "join" or game.join_open:
            await message.reply("🕯 You can begin only after joining is closed.")
            return

        if len(game.players) < 3:
            await message.reply("🕯 Not enough players to begin.")
            return

        # start round 1
        game.phase = "round"
        game.round = 1

        await message.reply(
            f"🐺 **The game has begun!**\n"
            f"👥 Players: {len(game.players)}\n"
            f"🔁 Round: {game.round}"
        )

        # DM all players with choices
        for user_id in game.players.keys():
            try:
                await app.send_message(
                    user_id,
                    ROUND_DM_TEXT,
                    reply_markup=dm_options_keyboard()
                )
            except:
                pass  # user blocked bot / never started DM
