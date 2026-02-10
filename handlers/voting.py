import asyncio
from utils.keyboards import vote_kb
from config import VOTE_TIME
from handlers.end import end_game

async def start_vote(app, game):
    game.votes.clear()

    for uid in game.alive:
        await app.send_message(
            uid,
            "🗳 Vote:",
            reply_markup=vote_kb({u: game.players[u] for u in game.alive})
        )

    await asyncio.sleep(VOTE_TIME)
    await end_game(app, game)
