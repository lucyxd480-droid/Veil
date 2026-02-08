from pyrogram import filters
from core.state import game
from utils.text import ROUND_DM_TEXT
from utils.keyboards import dm_options_keyboard


def register_begin(app):

    @app.on_message(filters.group & filters.command("begin"))
    async def begin(_, msg):

        if game.phase != "ready":
            await msg.reply("🕯 You cannot begin yet.")
            return

        if len(game.players) < 3:
            await msg.reply("🕯 Not enough players.")
            return

        game.phase = "round"
        game.round = 1

        await msg.reply(
            f"🐺 **The game has begun!**\n"
            f"👥 Players: {len(game.players)}\n"
            f"🔁 Round: {game.round}"
        )

        for user_id in game.players:
            try:
                await app.send_message(
                    user_id,
                    ROUND_DM_TEXT,
                    reply_markup=dm_options_keyboard()
                )
            except:
                pass
