from core.state import game
from utils.text import END_TRUST, END_BETRAY, END_SILENT

def check_end(app):
    if game.round > game.max_rounds or game.trust_collapse >= 2:
        winner = max(game.influence, key=game.influence.get, default=None)
        end(app, winner)
        return True

    game.round += 1
    return False

def end(app, winner):
    if winner:
        end_text = END_TRUST
    else:
        end_text = END_SILENT

    app.send_message(game.chat_id, end_text)
    game.reset()
