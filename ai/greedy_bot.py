import random
from ai.bot import BaseBot
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category


class GreedyBot(BaseBot):
    def __init__(self):
        super().__init__("GreedyBot")

    def choose_action(self, game_state):
        # jeśli można jeszcze rzucać – losuj
        if game_state.rolls_left > 0:
            hold = [random.choice([True, False]) for _ in range(5)]
            return Action(ActionType.ROLL, hold)

        # w przeciwnym razie najwyzszy dostepny wynik

        high_name = ""
        high_score = -1
        for cat in Category:
            if game_state.score_table.is_available(cat):
                score = score_category(game_state.dice, cat)
                if score > high_score:
                    high_score = score
                    high_name = cat

        return Action(ActionType.SELECT_CATEGORY, high_name)