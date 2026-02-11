import asyncio

from core.engine import assign_roles
from core.horror import horror
from core.state import games, new_game_state
from core.wincheck import check_win


def _alive_players(game):
    return [uid for uid in game["alive"] if uid in game["players"]]


async def schedule_join_expiry(app, chat_id: int, seconds: int):
    game = games[chat_id]
    old = game.get("join_task")
    if old and not old.done():
        old.cancel()

    async def _join_timeout():
        await asyncio.sleep(seconds)
        game = games.get(chat_id)
        if not game or game.get("phase") != "join" or game.get("started"):
            return
        if len(game["players"]) < game["min_players"]:
            game["phase"] = "idle"
            await app.send_message(
                chat_id,
                "❌ Join timer ended. Not enough players. Start again with /startgame."
            )
            return
        await start_game(app, chat_id)

    game["join_task"] = asyncio.create_task(_join_timeout())


async def start_game(app, chat_id: int):
    game = games.get(chat_id)
    if not game or game.get("started"):
        return False

    players = list(game["players"].keys())
    if len(players) < game["min_players"]:
        return False

    game["roles"] = assign_roles(players)
    game["started"] = True
    game["round"] = 1

    for uid, role in game["roles"].items():
        if uid in game["role_sent"]:
            continue
        game["role_sent"].add(uid)
        await app.send_message(uid, f"🕯 Your role: {role}")

    await app.send_message(chat_id, "🕯 The game begins. Night phase starts now.")
    await start_night(app, chat_id)
    return True


async def start_night(app, chat_id: int):
    game = games.get(chat_id)
    if not game:
        return

    game["phase"] = "night"
    game["night_actions"] = {}

    from handlers.night_actions import send_night_action_buttons
    await send_night_action_buttons(app, chat_id)
    await app.send_message(chat_id, f"🌑 Night {game['round']} has started.")
    await schedule_phase(app, chat_id, 45, resolve_night)


async def resolve_night(app, chat_id: int):
    game = games.get(chat_id)
    if not game or game.get("phase") != "night":
        return

    actions = game.get("night_actions", {})
    kill_targets = [
        target for action, target in actions.values()
        if action == "kill" and target in game["alive"]
    ]

    if kill_targets:
        target = kill_targets[0]
        game["alive"].discard(target)
        name = game["players"].get(target, {}).get("name", "A player")
        await app.send_message(chat_id, f"☠️ {name} was found at dawn.")
    else:
        await app.send_message(chat_id, "🌫 No one died tonight.")

    result = check_win(chat_id)
    if result:
        await announce_winner(app, chat_id, result)
        return

    await start_discussion(app, chat_id)


async def start_discussion(app, chat_id: int):
    game = games.get(chat_id)
    if not game:
        return

    game["phase"] = "discussion"
    await app.send_message(chat_id, f"🧠 Discussion phase. {horror()}")
    await schedule_phase(app, chat_id, 35, start_vote)


async def start_vote(app, chat_id: int):
    from utils.keyboards import pick_kb

    game = games.get(chat_id)
    if not game:
        return

    game["phase"] = "vote"
    game["picks"] = {}

    alive_names = [game["players"][uid]["name"] for uid in _alive_players(game)]
    if not alive_names:
        await app.send_message(chat_id, "No one is left to vote.")
        return

    await app.send_message(
        chat_id,
        "⚖️ Voting phase. Choose the condemned:",
        reply_markup=pick_kb(alive_names)
    )
    await schedule_phase(app, chat_id, 30, resolve_vote)


async def resolve_vote(app, chat_id: int):
    game = games.get(chat_id)
    if not game or game.get("phase") != "vote":
        return

    tally = {}
    for voted_name in game.get("picks", {}).values():
        tally[voted_name] = tally.get(voted_name, 0) + 1

    if tally:
        condemned = max(tally.items(), key=lambda x: x[1])[0]
        condemned_id = next(
            (uid for uid, p in game["players"].items() if p["name"] == condemned and uid in game["alive"]),
            None
        )
        if condemned_id is not None:
            game["alive"].discard(condemned_id)
            await app.send_message(chat_id, f"🔥 {condemned} has been condemned by vote.")
    else:
        await app.send_message(chat_id, "🌫 No votes were cast. The Veil tightens.")

    result = check_win(chat_id)
    if result:
        await announce_winner(app, chat_id, result)
        return

    game["round"] += 1
    await start_night(app, chat_id)


async def announce_winner(app, chat_id: int, result: str):
    text = "🤍 Innocents have won the game." if result == "innocents" else "🩸 Evil has consumed the town."
    await app.send_message(chat_id, text)

    game = games.get(chat_id)
    if game:
        t = game.get("phase_task")
        if t and not t.done():
            t.cancel()

    games[chat_id] = new_game_state()


async def schedule_phase(app, chat_id: int, seconds: int, callback):
    game = games.get(chat_id)
    if not game:
        return

    old = game.get("phase_task")
    if old and not old.done():
        old.cancel()

    async def _phase_timeout():
        await asyncio.sleep(seconds)
        await callback(app, chat_id)

    game["phase_task"] = asyncio.create_task(_phase_timeout())
