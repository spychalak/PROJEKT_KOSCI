import random
from ai.bot import BaseBot
from game.actions import Action, ActionType
from game.categories import Category


class RandomBot(BaseBot):
    def __init__(self):
        super().__init__("RandomBot")

    def choose_action(self, game_state):
        # jeśli można jeszcze rzucać – losuj
        if game_state.rolls_left > 0:
            hold = [random.choice([True, False]) for _ in range(5)]
            return Action(ActionType.ROLL, hold)

        # w przeciwnym razie losowa dostępna kategoria
        available = [
            cat for cat in Category
            if game_state.score_table.is_available(cat)
        ]
        cat = random.choice(available)
        return Action(ActionType.SELECT_CATEGORY, cat)