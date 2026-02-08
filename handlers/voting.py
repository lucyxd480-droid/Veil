from pyrogram import filters
from core.state import game

def start_voting(app):
    game.votes.clear()

    app.send_message(
        game.chat_id,
        "🗳 **The Veil invites judgment**\n"
        "Vote to weaken one presence.\n\n"
        "Use: `/vote @username`"
    )


def register_voting(app):

    @app.on_message(filters.command("vote") & filters.group)
    async def vote(_, msg):
        if not msg.entities or len(msg.entities) < 2:
            return await msg.reply("Invalid vote.")

        target = msg.entities[1].user
        if not target or target.id not in game.players:
            return await msg.reply("Invalid target.")

        game.influence[target.id] -= 20
        await msg.reply("🕯 Judgment has been cast.")
