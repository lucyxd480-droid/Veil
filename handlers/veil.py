import asyncio, random
from pyrogram import filters
from core.state import games
from utils.keyboards import choice_kb
from utils.texts import ROLE_TEXT
from config import CHOICE_TIME, TRAITOR_RATIO
from handlers.vote import start_vote

def register_veil(app):

    @app.on_callback_query(filters.regex("^enter$"))
    async def enter(_, cq):
        game = games.get(cq.message.chat.id)
        uid = cq.from_user.id
        if not game or uid not in game.alive or game.round_lock:
            return

        if game.round == 0:
            assign_roles(app, game)

        await cq._client.send_message(uid, f"🕯 Round {game.round+1}", reply_markup=choice_kb())

        if not game.round_lock:
            game.round_lock = True
            asyncio.create_task(round_timer(app, game))

    @app.on_callback_query(filters.regex("^(trust|betray|silent)$"))
    async def choose(_, cq):
        game = games.get(cq.message.chat.id)
        if game:
            game.choices[cq.from_user.id] = cq.data
            await cq.answer("Locked.")

async def round_timer(app, game):
    await asyncio.sleep(CHOICE_TIME)
    await resolve_round(app, game)

def assign_roles(app, game):
    uids = list(game.players.keys())
    random.shuffle(uids)

    traitors = max(1, len(uids)//TRAITOR_RATIO)
    roles = (
        ["traitor"] * traitors +
        ["guardian", "watcher", "jester", "judge", "shadow"]
    )

    for uid in uids:
        role = roles.pop(0) if roles else "innocent"
        game.roles[uid] = role
        app.send_message(uid, ROLE_TEXT[role])

async def resolve_round(app, game):
    game.round += 1

    for uid in game.alive:
        game.choices.setdefault(uid, "silent")

    betray = [u for u,c in game.choices.items() if c == "betray"]
    victim = None

    if betray:
        victim = random.choice(list(game.alive - set(betray)))

        if game.roles.get(victim) == "shadow" and victim not in game.shadow_used:
            game.shadow_used.add(victim)
        elif game.roles.get(victim) == "guardian" and not game.guardian_used:
            game.guardian_used = True
        else:
            game.alive.remove(victim)

    game.choices.clear()
    game.round_lock = False

    await app.send_message(game.chat_id, f"🕯 Round {game.round} ended.")

    if len(game.alive) <= 2:
        await start_vote(app, game)
