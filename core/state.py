import time
import asyncio

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        # group info
        self.chat_id = None

        # players
        self.players = {}  # user_id: name

        # join phase
        self.join_open = False
        self.join_duration = 30
        self.extend_duration = 15
        self.join_end_time = None
        self.extended = False
        self.join_task = None

        # game
        self.round = 0
        self.phase = "idle"

game = GameState()
