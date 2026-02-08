import time

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chat_id = None
        self.players = {}        # user_id: name
        self.influence = {}      # user_id: points
        self.join_open = False
        self.join_duration = 60
        self.join_end_time = None
        self.join_extended = 0
        self.phase = "idle"
        self.round = 0
        self.choices = {}        
        self.votes = {}          
        self.trust_collapse = 0
        self.max_rounds = 5

game = GameState()
