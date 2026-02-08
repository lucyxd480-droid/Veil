from pyrogram import filters
from core.state import game
from utils.text import DM_JOIN_TEXT

def register_dm_join(app):

    @app.on_message(filters.private & filters.command("start"))
    async def dm_start(_, message):
        if message.text != "/start join":
            return

        user = message.from_user

        if not game.join_open:
            await message.reply("🕯 The Veil is closed.")
            return

        if user.id in game.players:
            await message.reply("🕯 You are already inside.")
            return

        game.players[user.id] = user.first_name or f"({user.id})"
        game.influence[user.id] = 100

        await message.reply(DM_JOIN_TEXT)

        players = "\n".join(f"• {n}" for n in game.players.values())
        await app.send_message(
            game.chat_id,
            f"#Players: {len(game.players)}\n{players}"
        )

    @app.on_message(filters.private & filters.command("leavegame"))
    async def leave_dm(_, message):
        user = message.from_user
        if user.id in game.players:
            del game.players[user.id]
            del game.influence[user.id]
            await message.reply("🕯 You left the game.")
        else:
            await message.reply("🕯 You are not in the game.")
