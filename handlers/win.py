from pyrogram import filters
from core.wincheck import check_win


def register_win(app):

    @app.on_message(filters.command("win") & filters.group)
    async def win_handler(_, msg):
        result = check_win(msg.chat.id)

        if result == "innocents":
            await msg.reply("🤍 Innocents have won the game.")
        elif result == "traitors":
            await msg.reply("🩸 Evil has consumed the town.")
        else:
            await msg.reply("🕯 The game is still ongoing.")
