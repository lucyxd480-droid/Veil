from dataclasses import dataclass

@dataclass
class Player:
    user_id: int
    name: str
    influence: int = 50
    silent_streak: int = 0
