import asyncio
import time
from pyrogram import filters

from core.state import game
from utils.text import DM_JOIN_TEXT
from handlers.join_timer import start_join_timer


def register_dm_join(app):

    @app.on_message(filters.private & filters.command("start"))
    async def dm_start(client, message):
        if message.text != "/start join":
            return

        user = message.from_user

        if not game.join_open:
            await message.reply("🕯 The Veil is closed.")
            return

        if user.id in game.players:
            await message.reply("You are already inside the Veil.")
            return

        # add player
        game.players[user.id] = user.first_name
        await message.reply(DM_JOIN_TEXT)

        # update group player list
        await update_player_list(app)


async def update_player_list(app):
    if not game.chat_id:
        return

    players = "\n".join(
        f"• {name}" for name in game.players.values()
    )

    text = (
        "🕯 **Players in the Veil**\n\n"
        f"{players}\n\n"
        f"👥 Total: {len(game.players)}"
    )

    await app.send_message(game.chat_id, text)
