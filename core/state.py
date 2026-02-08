import time

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chat_id = None
        self.players = {}        # user_id: username
        self.join_open = False
        self.join_duration = 60  # 60 sec default
        self.join_end_time = None
        self.join_extended = 0
        self.phase = "idle"
        self.round = 0
        self.choices = {}        # user_id: choice
        self.votes = {}          # user_id: vote target
        self.influence = {}      # user_id: influence points
        self.trust_collapse = 0
        self.max_rounds = 5

game = GameState()
