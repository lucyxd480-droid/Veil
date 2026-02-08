from core.state import game

def check_end(app):
    if game.round > game.max_rounds or game.trust_collapse >= 2:
        winner = max(game.influence, key=game.influence.get, default=None)
        end(app, winner)
        return True

    game.round += 1
    return False

def end(app, winner):
    if winner:
        text = f"🏆 Winner: {game.players[winner]}"
    else:
        text = "No winner emerged."

    app.send_message(game.chat_id, text)
    game.reset()
