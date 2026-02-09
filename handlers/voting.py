import asyncio
import time

from pyrogram import filters
from core.state import game

VOTE_TIME = 20


async def start_voting(app):
    game.phase = "voting"
    game.votes.clear()
    game.vote_deadline = time.time() + VOTE_TIME

    await app.send_message(
        game.chat_id,
        f"🗳 Voting phase started!\nUse `/vote @username` in next {VOTE_TIME} sec."
    )

    asyncio.create_task(voting_timer(app))


async def voting_timer(app):
    await asyncio.sleep(VOTE_TIME)

    if game.phase != "voting":
        return

    counts = {}
    for target_id in game.votes.values():
        counts[target_id] = counts.get(target_id, 0) + 1

    if counts:
        target_id = max(counts, key=counts.get)
        game.influence[target_id] = max(0, game.influence.get(target_id, 100) - 20)
        name = game.players.get(target_id, str(target_id))
        await app.send_message(
            game.chat_id,
            f"⚖️ Vote result: {name} loses 20 influence. Remaining: {game.influence[target_id]}"
        )

        if game.influence[target_id] <= 0:
            game.players.pop(target_id, None)
            game.usernames.pop(target_id, None)
            game.influence.pop(target_id, None)
            await app.send_message(game.chat_id, f"💀 {name} has been eliminated.")
    else:
        await app.send_message(game.chat_id, "⚖️ No votes were cast this round.")

    from handlers.endgame import check_end
    from handlers.dm_round import start_round

    if await check_end(app):
        return

    game.round += 1
    await start_round(app)


def register_voting(app):

    @app.on_message(filters.group & filters.command("vote"))
    async def vote(_, msg):
        if game.phase != "voting":
            return await msg.reply("Voting is not active right now.")

        voter = msg.from_user
        if not voter or voter.id not in game.players:
            return await msg.reply("Only active players can vote.")

        parts = (msg.text or "").split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            return await msg.reply("Usage: /vote @username")

        target_username = parts[1][1:].lower()
        target_id = None
        for uid, username in game.usernames.items():
            if username and username.lower() == target_username:
                target_id = uid
                break

        if not target_id or target_id not in game.players:
            return await msg.reply("Invalid target username.")

        if target_id == voter.id:
            return await msg.reply("You cannot vote yourself.")

        game.votes[voter.id] = target_id
        await msg.reply("✅ Vote recorded.")
