class GameState:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.reset()

    def reset(self):
        self.players = {}
        self.alive = set()
        self.roles = {}
        self.choices = {}
        self.votes = {}
        self.round = 0
        self.round_lock = False
        self.active = False
        self.guardian_used = False
        self.shadow_used = set()

games = {}
