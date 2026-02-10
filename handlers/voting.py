import asyncio
import time

from pyrogram import filters
from core.state import game

VOTE_TIME = 120  # 2 minutes


async def start_voting(app):
    game.phase = "voting"
    game.votes.clear()
    game.vote_deadline = time.time() + VOTE_TIME

    await app.send_message(
        game.chat_id,
        "🗳 Voting phase started!\n"
        "Use `/vote @username`, mention a player, or reply with `/vote`.\n"
        "Voting closes early if all active players vote."
    )

    asyncio.create_task(voting_timer(app))


async def voting_timer(app):
    await asyncio.sleep(VOTE_TIME)

    if game.phase != "voting":
        return

    await finalize_voting(app)


async def finalize_voting(app):
    if game.phase != "voting":
        return

    game.phase = "resolving_vote"

    counts = {}
    for target_id in game.votes.values():
        counts[target_id] = counts.get(target_id, 0) + 1

    if counts:
        target_id = max(counts, key=counts.get)
        game.influence[target_id] = max(
            0, game.influence.get(target_id, 100) - 20
        )

        name = game.players.get(target_id, str(target_id))
        await app.send_message(
            game.chat_id,
            f"⚖️ Vote result: {name} loses 20 influence. "
            f"Remaining: {game.influence[target_id]}"
        )

        if game.influence[target_id] <= 0:
            game.players.pop(target_id, None)
            game.usernames.pop(target_id, None)
            game.influence.pop(target_id, None)
            await app.send_message(
                game.chat_id,
                f"💀 {name} has been eliminated."
            )
    else:
        await app.send_message(
            game.chat_id,
            "⚖️ No votes were cast this round."
        )

    from handlers.endgame import check_end
    from handlers.dm_round import announce_round_start

    if await check_end(app):
        return

    game.round += 1
    await announce_round_start(app)


def register_voting(app):

    @app.on_message(filters.group & filters.command("vote"))
    async def vote(_, msg):
        if game.phase != "voting":
            return await msg.reply("Voting is not active right now.")

        voter = msg.from_user
        if not voter or voter.id not in game.players:
            return await msg.reply("Only active players can vote.")

        target_id = resolve_vote_target(msg)
        if not target_id or target_id not in game.players:
            return await msg.reply(
                "Invalid target. Use @username, mention, or reply with /vote."
            )

        if target_id == voter.id:
            return await msg.reply("You cannot vote yourself.")

        game.votes[voter.id] = target_id
        await msg.reply("✅ Vote recorded.")

        if len(game.votes) >= len(game.players):
            await app.send_message(
                game.chat_id,
                "⏩ All players voted. Closing voting early."
            )
            await finalize_voting(app)


def resolve_vote_target(msg):
    # 1) Reply vote: /vote as reply to a user's message
    if msg.reply_to_message and msg.reply_to_message.from_user:
        return msg.reply_to_message.from_user.id

    # 2) Mention entities (@username or text mention)
    entities = msg.entities or []
    for ent in entities:
        ent_type = str(ent.type).lower()

        if ent_type.endswith("text_mention") and getattr(ent, "user", None):
            return ent.user.id

        if ent_type.endswith("mention") and not ent_type.endswith("text_mention"):
            mention_text = (msg.text or "")[
                ent.offset: ent.offset + ent.length
            ]
            username = mention_text.lstrip("@").lower()
            for uid, known_username in game.usernames.items():
                if known_username and known_username.lower() == username:
                    return uid

    # 3) Fallback: /vote @username
    parts = (msg.text or "").split()
    if len(parts) >= 2 and parts[1].startswith("@"):
        username = parts[1][1:].lower()
        for uid, known_username in game.usernames.items():
            if known_username and known_username.lower() == username:
                return uid

    return None
