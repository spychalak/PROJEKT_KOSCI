import random
from collections import defaultdict
from ai.bot import BaseBot
from ai.strategy import Strategy
from ai.patterns import detect_pattern
from ai.heu_exec import (
    hunt_same, hunt_straight,
    best_available_category, worst_available_category
)
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category


class LearningBotRL_plus_Heu(BaseBot):
    def __init__(
        self,
        alpha=0.1,
        gamma=0.9,
        epsilon_start=0.6,
        epsilon_min=0.05,
        epsilon_decay=0.999
    ):
        super().__init__("RL+HeuristicBot")

        self.Q = defaultdict(float)

        self.alpha = alpha
        self.gamma = gamma

        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.last_state = None
        self.last_strategy = None

    # STAN DLA RL
    def encode_state(self, state):
        pattern = detect_pattern(state.dice)
        rolls = state.rolls_left

        filled = sum(
            1 for cat in Category
            if not state.score_table.is_available(cat)
        )

        if filled < 4:
            phase = "EARLY"
        elif filled < 9:
            phase = "MID"
        else:
            phase = "LATE"

        return pattern, rolls, phase

    # WYBÓR STRATEGII
    def choose_strategy(self, state):
        s = self.encode_state(state)

        if random.random() < self.epsilon:
            strat = random.choice(list(Strategy))
        else:
            strat = max(
                Strategy,
                key=lambda st: self.Q[(s, st)]
            )

        self.last_state = s
        self.last_strategy = strat
        return strat

    # GŁÓWNA DECYZJA
    def choose_action(self, state):
        strat = self.choose_strategy(state)

        # RZUTY
        if state.rolls_left > 0:
            if strat == Strategy.HUNT_GENERAL:
                return Action(ActionType.ROLL, hunt_same(state.dice, 3))

            if strat == Strategy.HUNT_FOUR_KIND:
                return Action(ActionType.ROLL, hunt_same(state.dice, 2))

            if strat == Strategy.HUNT_STRAIGHT:
                return Action(ActionType.ROLL, hunt_straight(state.dice))

            return Action(ActionType.ROLL, [True]*5)

        # WYBÓR KATEGORII
        cat = None  # <-- KLUCZOWE ZABEZPIECZENIE

        filled = sum(
            1 for c in Category
            if not state.score_table.is_available(c)
        )

        if strat == Strategy.DUMP_BAD and filled >= 9:
            cat = worst_available_category(state)
        else:
            cat = best_available_category(state)

        return Action(ActionType.SELECT_CATEGORY, cat)

    # UCZENIE
    def learn(self, reward, next_state):
        if self.last_state is None:
            return

        s = self.last_state
        s2 = self.encode_state(next_state)
        a = self.last_strategy

        future = max(
            self.Q[(s2, st)] for st in Strategy
        )

        self.Q[(s, a)] += self.alpha * (
            reward + self.gamma * future - self.Q[(s, a)]
        )

    def end_episode(self):
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )