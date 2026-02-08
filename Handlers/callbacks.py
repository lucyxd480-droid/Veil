from pyrogram import filters
from core.engine import GAMES

def register_callbacks(app):

    @app.on_callback_query(filters.regex("^d_"))
    async def decision(_, q):
        state = GAMES.get(q.message.chat.id)
        if not state or state.phase != "decision":
            return
        state.choices[q.from_user.id] = q.data[2:]
        await q.answer("Your intent is hidden.")

    @app.on_callback_query(filters.regex("^v_"))
    async def vote(_, q):
        state = GAMES.get(q.message.chat.id)
        if not state or state.phase != "voting":
            return
        state.votes[q.from_user.id] = int(q.data[2:])
        await q.answer("The Veil has noted this.")
