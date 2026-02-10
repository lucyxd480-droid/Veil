from pyrogram import filters
from core.leaderboard import top_players

def register_leaderboard(app):
    @app.on_message(filters.command("leaderboard"))
    async def lb(_, msg):
        text = "🏆 LEADERBOARD\n\n"
        for i,(uid,w) in enumerate(top_players(),1):
            text += f"{i}. {uid} — {w} wins\n"
        await msg.reply(text)
