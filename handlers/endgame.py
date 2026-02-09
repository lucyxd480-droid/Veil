from core.state import game
from utils.text import END_BETRAY, END_SILENT, END_TRUST

async def check_end(app):
    if len(game.players) < 3:
        await app.send_message(game.chat_id, "🕯 Too few players left. Game ended.")
        game.reset()
        return True

    if game.round >= game.max_rounds:
        winner = max(game.influence, key=game.influence.get, default=None)
        await end(app, winner, reason="rounds")
        return True

    if game.trust_collapse >= 2:
        await end(app, None, reason="collapse")
        return True

    return False


async def end(app, winner, reason: str):
    if reason == "collapse":
        end_text = END_BETRAY
    elif winner:
        win_name = game.players.get(winner, "Unknown")
        end_text = f"{END_TRUST}\n\n🏆 Winner: {win_name}"
    else:
        end_text = END_SILENT

    await app.send_message(game.chat_id, end_text)
    game.reset()
