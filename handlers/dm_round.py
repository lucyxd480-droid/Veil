import asyncio, time, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.state import game
from handlers.voting import start_voting
from handlers.endgame import check_end
from utils.text import GROUP_ROUND_RESULT

CHOICE_TIME = 40

def dm_options_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Trust", callback_data="c_trust")],
        [InlineKeyboardButton("🔴 Betray", callback_data="c_betray")],
        [InlineKeyboardButton("⚫ Remain Silent", callback_data="c_silent")]
    ])

def register_dm_round(app):

    @app.on_callback_query(filters.regex("^c_"))
    async def handle_choice(_, cb):
        uid = cb.from_user.id
        if game.phase != "round":
            return await cb.answer("🕯 Round not active.")
        if uid not in game.players:
            return await cb.answer("🕯 You are not in the game.")

        game.choices[uid] = cb.data.replace("c_", "")
        await cb.answer("🕯 Choice recorded.")

async def start_round(app):
    game.choices.clear()
    game.choice_deadline = time.time() + CHOICE_TIME

    for uid in game.players:
        await app.send_message(
            uid,
            f"🕯 Round {game.round}\nYou have {CHOICE_TIME} seconds to choose.",
            reply_markup=dm_options_keyboard()
        )

    await asyncio.sleep(CHOICE_TIME)

    for uid in game.players:
        if uid not in game.choices:
            game.choices[uid] = "silent"

    text = random.choice(GROUP_ROUND_RESULT)
    await app.send_message(game.chat_id, f"🕯 Round {game.round} results:\n{text}")

    if check_end(app):
        return

    start_voting(app)
