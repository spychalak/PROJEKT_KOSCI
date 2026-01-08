from enum import Enum, auto
from game.categories import Category
class Action:
    ROLL = auto()
    SELECT_CATEGORY = auto()

    def __init__(self, action_type, category: Category):
        self.type = action_type
        self.category = category
