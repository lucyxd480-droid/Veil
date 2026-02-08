import asyncio, time
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.state import game
from handlers.voting import start_voting
from handlers.endgame import check_end

CHOICE_TIME = 40

def start_round(app):
    game.choice_deadline = time.time() + CHOICE_TIME

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Trust", callback_data="c_trust")],
        [InlineKeyboardButton("🔴 Betray", callback_data="c_betray")],
        [InlineKeyboardButton("⚫ Remain Silent", callback_data="c_silent")]
    ])

    for uid in game.players:
        app.send_message(
            uid,
            f"🕯 **Round {game.round}**\n\n"
            "You have 40 seconds.\nChoose carefully.",
            reply_markup=keyboard
        )

    asyncio.create_task(round_timer(app))


async def round_timer(app):
    await asyncio.sleep(CHOICE_TIME)

    for uid in game.players:
        if uid not in game.choices:
            game.choices[uid] = "silent"

    await reveal(app)


def register_dm_round(app):

    @app.on_callback_query(filters.regex("^c_"))
    async def handle_choice(_, cb):
        uid = cb.from_user.id

        if uid in game.choices:
            return await cb.answer("Choice already sealed.")

        if time.time() > game.choice_deadline:
            return await cb.answer("Time is over.")

        game.choices[uid] = cb.data.replace("c_", "")
        await cb.answer("🕯 Choice sealed.")


async def reveal(app):
    values = list(game.choices.values())
    trust = values.count("trust")
    betray = values.count("betray")
    silent = values.count("silent")

    if betray > trust:
        text = "🔴 **A betrayal went unnoticed.**"
        game.trust_collapse += 1
    elif silent >= trust:
        text = "⚫ **Silence shifted the balance.**"
        game.trust_collapse += 1
    else:
        text = "🟢 **Some trust was misplaced.**"
        game.trust_collapse = 0

    await app.send_message(
        game.chat_id,
        f"🕯 **The Veil Shifts…**\n\n{text}"
    )

    if check_end(app):
        return

    start_voting(app)
