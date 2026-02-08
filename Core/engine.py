import asyncio
from core.influence import apply_choice
from core.disclosure import disclosure
from utils.keyboards import decision_kb, vote_kb
from config import ROUND_TIME, VOTE_TIME, MAX_ROUNDS

GAMES = {}  # chat_id -> GameState

async def run_game(app, state):
    state.active = True

    while state.round < MAX_ROUNDS:
        state.round += 1
        state.phase = "decision"
        state.choices.clear()
        state.votes.clear()

        # Send decisions
        for p in state.players.values():
            await app.send_message(
                p.user_id,
                f"Round {state.round}: Choose wisely.",
                reply_markup=decision_kb()
            )

        await asyncio.sleep(ROUND_TIME)

        for uid, choice in state.choices.items():
            apply_choice(state.players[uid], choice)

        await app.send_message(state.chat_id, disclosure())

        state.phase = "voting"
        await app.send_message(
            state.chat_id,
            "Apply pressure.",
            reply_markup=vote_kb(state.players)
        )

        await asyncio.sleep(VOTE_TIME)

        for target in state.votes.values():
            state.players[target].influence = max(
                0, state.players[target].influence - 6
            )

    await end_game(app, state)
