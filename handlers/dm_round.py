import asyncio
import random
import time

from pyrogram import filters
from core.state import game
from handlers.endgame import check_end
from handlers.voting import start_voting
from utils.keyboards import dm_options_keyboard, enter_veil_keyboard
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

        await cb.message.edit_text(
            f"✅ You selected: **{game.choices[uid].title()}**\n"
            "Your choice is locked for this round."
        )

    @app.on_callback_query(filters.regex("^enter_veil$"))
    async def enter_veil(_, cb):
        uid = cb.from_user.id

        if uid not in game.players:
            return await cb.answer("You are not part of this game.", show_alert=True)

        if game.phase != "round":
            return await cb.answer(
                "Round selection is not active right now.",
                show_alert=True
            )

        try:
            await cb._client.send_message(
                uid,
                f"🕯 Round {game.round}\nChoose within {CHOICE_TIME} seconds.",
                reply_markup=dm_options_keyboard()
            )
            await cb.answer(
                "Check your DM to select your role.",
                show_alert=False
            )
        except Exception:
            await cb.answer(
                "Please start the bot in DM first: /start",
                show_alert=True
            )


async def announce_round_start(app):
    await app.send_message(
        game.chat_id,
        f"🕯 **Round {game.round} started!**\n"
        "Choose wisely... shadows are watching.\n\n"
        "Tap below to enter Veil and make your choice.",
        reply_markup=enter_veil_keyboard("Enter Veil")
    )

    await start_round(app)


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
                game.influence[uid] = max(
                    0, game.influence.get(uid, 100) - 20
                )

    if silent == len(game.players):
        game.trust_collapse += 1

    trust_list = _format_choice_players("trust")
    betray_list = _format_choice_players("betray")
    silent_list = _format_choice_players("silent")

    flavor = random.choice(GROUP_ROUND_RESULT)

    await app.send_message(
        game.chat_id,
        f"🕯 Round {game.round} result\n"
        f"Trust: {trust} | Betray: {betray} | Silent: {silent}\n"
        f"Collapse: {game.trust_collapse}/2\n\n"
        f"🤝 Trust: {trust_list}\n"
        f"🗡 Betray: {betray_list}\n"
        f"🤫 Silent: {silent_list}\n\n"
        f"{flavor}"
    )

    if await check_end(app):
        return

    await start_voting(app)


def _display_name(uid: int):
    username = game.usernames.get(uid)
    if username:
        return f"@{username}"
    return game.players.get(uid, str(uid))


def _format_choice_players(choice: str):
    members = [
        _display_name(uid)
        for uid, picked in game.choices.items()
        if picked == choice
    ]
    return ", ".join(members) if members else "None"
