import time


class GameState:
    def __init__(self, chat_id=None):
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

    def start_game(self):
        """Start the actual game"""
        self.active = True
        self.phase = "game"
        self.round = 1
        self.choices.clear()
        self.votes.clear()

    def reset(self):
        self.__init__(self.chat_id)


# global shared state
game = GameState()
