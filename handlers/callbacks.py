from pyrogram import filters
from core.engine import GAMES
from core.state import game
import time

def register_callbacks(app):

    # 🎃 JOIN GAME (lobby phase)
    @app.on_callback_query(filters.regex("^join_game$"))
    async def join_game_cb(_, query):
        user = query.from_user

        if not game.join_open:
            await query.answer("💀 Joining closed", show_alert=True)
            return

        if user.id in game.players:
            await query.answer("🎀 Already joined", show_alert=True)
            return

        game.players[user.id] = user.first_name
        await query.answer("✅ Joined successfully!")

        await query.message.edit_text(
            f"🎃 **Game Lobby**\n"
            f"👥 Players: {len(game.players)}\n"
            f"⏳ Time left: {int(game.join_end_time - time.time())}s",
            reply_markup=query.message.reply_markup
        )

    # 🎭 DECISION PHASE
    @app.on_callback_query(filters.regex("^d_"))
    async def decision(_, q):
        state = GAMES.get(q.message.chat.id)
        if not state or state.phase != "decision":
            return
        state.choices[q.from_user.id] = q.data[2:]
        await q.answer("Your intent is hidden.")

    # 🗳️ VOTING PHASE
    @app.on_callback_query(filters.regex("^v_"))
    async def vote(_, q):
        state = GAMES.get(q.message.chat.id)
        if not state or state.phase != "voting":
            return
        state.votes[q.from_user.id] = int(q.data[2:])
        await q.answer("The Veil has noted this.")
