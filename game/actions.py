from enum import Enum
from game.categories import Category


class ActionType(Enum):
    ROLL = 1
    SELECT_CATEGORY = 2


class Action:
    def __init__(self, action_type: ActionType, data=None):
        """
        data:
        - dla ROLL → lista booli [True/False] (czy trzymamy kostkę)
        - dla SELECT_CATEGORY → Category
        """
        self.type = action_type
        self.data = data
