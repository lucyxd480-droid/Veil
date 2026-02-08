from core.state import game

def check_end(app):
    if game.round > game.max_rounds or game.trust_collapse >= 2:
        winner = max(game.influence, key=game.influence.get, default=None)
        end(app, winner)
        return True

    game.reset_round()
    return False


def end(app, winner):
    if winner:
        text = (
            "🕯 **The Veil Falls…**\n\n"
            f"🏆 **Winner:** {game.players[winner]}\n"
            "Belief endured longer than doubt."
        )
    else:
        text = (
            "🕯 **The Veil Falls…**\n\n"
            "No presence stood firm.\nNo winner emerged."
        )

    app.send_message(game.chat_id, text)
    game.reset_game()
