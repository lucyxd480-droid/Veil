from pyrogram import filters
from core.state import game

def register_dm_join(app):

    @app.on_message(filters.command("start") & filters.private)
    async def dm_start(_, msg):

        if len(msg.command) < 2 or msg.command[1] != "veil_join":
            await msg.reply(
                "🕯 **Welcome to The Veil**\n\n"
                "Return to the group to join a game."
            )
            return

        user = msg.from_user

        if game.active:
            await msg.reply("⚫ The Veil is already sealed.")
            return

        if user.id in game.players:
            await msg.reply("😈 You are already inside The Veil.")
            return

        game.players[user.id] = user.first_name
        game.influence[user.id] = 100

        await msg.reply(
            "🕯 **Veil Joined Successfully**\n\n"
            "You have stepped beyond sight.\n"
            "Wait. Observe. Choose carefully."
        )
