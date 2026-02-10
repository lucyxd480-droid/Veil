from pyrogram import filters
from core.state import game
from handlers.dm_round import announce_round_start
from utils.keyboards import enter_veil_keyboard


def register_begin(app):

    @app.on_message(filters.group & filters.command("begin"))
    async def begin(_, msg):
        # Check if game is ready to begin
        if game.phase != "ready":
            return await msg.reply("🔹 You cannot begin yet.")

        if len(game.players) < 3:
            return await msg.reply("🙂 Not enough players to start the game.")

        # Set game phase and round
        game.phase = "round"
        game.round = 1

        # Announce game start in group
        await msg.reply(
            f"🕯 **The Veil has started.**\n"
            f"Go to bot DM and choose your role wisely.\n\n"
            f"Players: {len(game.players)}\n"
            f"Round: {game.round}",
            reply_markup=enter_veil_keyboard("Select your role")
        )

        # Start first round automatically
        await announce_round_start(app)
