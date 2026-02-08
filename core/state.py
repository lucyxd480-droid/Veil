class GameState:
    def __init__(self):
        self.chat_id = None
        self.players = {}        # user_id -> name
        self.influence = {}      # user_id -> score
        self.choices = {}        # user_id -> choice
        self.votes = {}          # user_id -> votes

        self.round = 1
        self.max_rounds = 3
        self.trust_collapse = 0
        self.choice_deadline = 0
        self.active = False

    def reset_round(self):
        self.choices.clear()
        self.votes.clear()
        self.round += 1

    def reset_game(self):
        self.__init__()

game = GameState()
