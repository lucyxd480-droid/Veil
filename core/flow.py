import asyncio

from core.engine import assign_roles
from core.horror import horror
from core.narrator import whisper
from core.roles import ROLES
from core.state import games, new_game_state
from core.wincheck import check_win


def _alive_players(game):
    return [uid for uid in game["alive"] if uid in game["players"]]


def _name(game, uid):
    return game["players"].get(uid, {}).get("name", "Unknown")


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
                "❌ The gate closed with too few souls. Start again with /startgame.",
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

    # Cancel pending join timer because game starts now.
    join_task = game.get("join_task")
    if join_task and not join_task.done():
        join_task.cancel()

    game["roles"] = assign_roles(players)
    game["started"] = True
    game["round"] = 1

    for uid, role in game["roles"].items():
        if uid in game["role_sent"]:
            continue
        game["role_sent"].add(uid)
        desc = ROLES.get(role, "Unknown role")
        await app.send_message(uid, f"🕯 Role: {role}\n{desc}")

    await app.send_message(chat_id, "🕯 The Veil rises. Roles are sent. Night begins now.")
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
    await app.send_message(chat_id, f"🌑 Night {game['round']} — {whisper()}")
    await schedule_phase(app, chat_id, 45, resolve_night)


async def resolve_night(app, chat_id: int):
    game = games.get(chat_id)
    if not game or game.get("phase") != "night":
        return

    actions = game.get("night_actions", {})

    kill_targets = [
        target
        for action, target in actions.values()
        if action == "kill" and target in game["alive"]
    ]
    protected = {
        target
        for action, target in actions.values()
        if action == "protect" and target in game["alive"]
    }
    watch_pairs = [
        (actor_id, target)
        for actor_id, (action, target) in actions.items()
        if action == "watch" and target in game["alive"]
    ]

    victim = None
    if kill_targets:
        candidate = kill_targets[0]
        if candidate in protected:
            await app.send_message(chat_id, "🛡 A guardian blocked death tonight.")
        else:
            victim = candidate

    for watcher_id, target in watch_pairs:
        role_seen = game.get("roles", {}).get(target, "unknown")
        await app.send_message(
            watcher_id,
            f"👁 You watched {_name(game, target)}. Aura detected: {role_seen}.",
        )

    if victim is not None:
        game["alive"].discard(victim)
        await app.send_message(chat_id, f"☠️ {_name(game, victim)} was found at dawn.")
    elif not kill_targets:
        await app.send_message(chat_id, "🌫 No blood touched the stone tonight.")

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
    await app.send_message(chat_id, f"🧠 Speak before judgment. {horror()}")
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
        await app.send_message(chat_id, "No one remains to judge.")
        return

    await app.send_message(
        chat_id,
        "⚖️ Day vote is open. Touch a name to condemn.",
        reply_markup=pick_kb(alive_names),
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
            (
                uid
                for uid, p in game["players"].items()
                if p["name"] == condemned and uid in game["alive"]
            ),
            None,
        )
        if condemned_id is not None:
            game["alive"].discard(condemned_id)
            await app.send_message(chat_id, f"🔥 {condemned} was consumed by the crowd.")
    else:
        await app.send_message(chat_id, "🌫 Silence wins. No one was condemned.")

    result = check_win(chat_id)
    if result:
        await announce_winner(app, chat_id, result)
        return

    game["round"] += 1
    await start_night(app, chat_id)


async def announce_winner(app, chat_id: int, result: str):
    game = games.get(chat_id)
    if result == "innocents":
        text = "🤍 Dawn breaks. The innocent outlived the monsters."
    else:
        text = "🩸 Darkness reigns. Evil owns the last breath."

    await app.send_message(chat_id, text)

    if game:
        for key in ("join_task", "phase_task"):
            task = game.get(key)
            if task and not task.done():
                task.cancel()

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
