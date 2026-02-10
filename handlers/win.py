from pyrogram import filters
from core.state import games
from core.wincheck import check_win

def register_win(app):
    @app.on_message(filters.command("win") & filters.group)
    async def win(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game:
            return

        result = check_win(game["alive"], game["roles"])
        if result:
            await msg.reply(f"🏁 {result} WINS")
