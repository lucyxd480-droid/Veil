class GameState:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.active = False
        self.round = 0
        self.players = {}
        self.choices = {}
        self.votes = {}
        self.phase = "idle"  # idle, decision, voting
