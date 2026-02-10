from core.leaderboard import add_win
from utils.texts import END_TEXT

async def end_game(app, game):
    winner = next(iter(game.alive))
    add_win(winner)

    await app.send_message(
        game.chat_id,
        f"{END_TEXT}\n👑 Winner: {game.players[winner]}"
    )

    game.reset()
