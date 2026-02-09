import asyncio
import random
import time

from pyrogram import filters
from core.state import game
from handlers.endgame import check_end
from handlers.voting import start_voting
from utils.keyboards import dm_options_keyboard
from utils.text import GROUP_ROUND_RESULT

CHOICE_TIME = 40

def register_dm_round(app):

    @app.on_callback_query(filters.regex("^c_"))
    async def handle_choice(_, cb):
        uid = cb.from_user.id
        if game.phase != "round":
            return await cb.answer("🕯 Round not active.", show_alert=False)
        if uid not in game.players:
            return await cb.answer("🕯 You are not in this game.", show_alert=False)

        game.choices[uid] = cb.data.replace("c_", "")
        await cb.answer("✅ Choice recorded.", show_alert=False)


async def start_round(app):
    game.phase = "round"
    game.choices.clear()
    game.choice_deadline = time.time() + CHOICE_TIME

    for uid in list(game.players.keys()):
        try:
            await app.send_message(
                uid,
                f"🕯 Round {game.round}\nChoose within {CHOICE_TIME} seconds.",
                reply_markup=dm_options_keyboard()
            )
        except Exception:
            game.choices[uid] = "silent"

    await asyncio.sleep(CHOICE_TIME)

    for uid in list(game.players.keys()):
        if uid not in game.choices:
            game.choices[uid] = "silent"

    trust = sum(1 for c in game.choices.values() if c == "trust")
    betray = sum(1 for c in game.choices.values() if c == "betray")
    silent = sum(1 for c in game.choices.values() if c == "silent")

    if trust > betray and trust > 0:
        for uid, choice in game.choices.items():
            if choice == "trust":
                game.influence[uid] = game.influence.get(uid, 100) + 10
    elif betray >= trust and betray > 0:
        game.trust_collapse += 1
        for uid, choice in game.choices.items():
            if choice == "trust":
                game.influence[uid] = max(0, game.influence.get(uid, 100) - 20)

    if silent == len(game.players):
        game.trust_collapse += 1

    flavor = random.choice(GROUP_ROUND_RESULT)
    await app.send_message(
        game.chat_id,
        f"🕯 Round {game.round} result\n"
        f"Trust: {trust} | Betray: {betray} | Silent: {silent}\n"
        f"Collapse: {game.trust_collapse}/2\n\n"
        f"{flavor}"
    )

    if await check_end(app):
        return

    await start_voting(app)
