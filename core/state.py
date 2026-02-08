import time

class GameState:
    def __init__(self, chat_id):
        self.chat_id = chat_id

        # lobby
        self.players = {}
        self.join_open = True
        self.join_duration = 30
        self.extend_duration = 15
        self.join_end_time = time.time() + self.join_duration
        self.extended = False

        # game
        self.active = False
        self.round = 0
        self.phase = "join"
        self.choices = {}
        self.votes = {}
