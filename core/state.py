import time

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chat_id = None

        self.players = {}  # user_id: name

        self.join_open = False
        self.join_duration = 30
        self.extend_duration = 15
        self.join_end_time = None
        self.extended = False

        self.phase = "idle"
        self.round = 0

game = GameState()
