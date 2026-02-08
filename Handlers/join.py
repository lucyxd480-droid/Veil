from pyrogram import filters
from models.player import Player
from core.engine import GAMES

def register_join(app):

    @app.on_message(filters.command("join") & filters.group)
    async def join(_, msg):
        state = GAMES.get(msg.chat.id)
        if not state or state.active:
            return

        user = msg.from_user
        if user.id not in state.players:
            state.players[user.id] = Player(user.id, user.first_name)
            await msg.reply(f"{user.first_name} stepped behind the Veil.")
