import random
from collections import defaultdict
from ai.bot import BaseBot
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category


def action_key(action):
    return action.type, tuple(action.data) if isinstance(action.data, list) else action.data


class LearningBotRL(BaseBot):
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.3):
        super().__init__("LearningBotRL")

        self.Q = defaultdict(float)
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount
        self.epsilon = epsilon  # eksploracja

        self.last_state = None
        self.last_action = None

    # ===============================
    # OBSERWACJA STANU
    # ===============================
    def encode_state(self, state):
        dice = tuple(sorted(state.dice))
        rolls = state.rolls_left
        available = tuple(
            int(state.score_table.is_available(cat))
            for cat in Category
        )
        return (dice, rolls, available)

    # ===============================
    # GENEROWANIE AKCJI
    # ===============================
    def possible_actions(self, state):
        actions = []

        if state.rolls_left > 0:
            actions += [
                Action(ActionType.ROLL, [False]*5),          # rzuć wszystko
                Action(ActionType.ROLL, [d >= 5 for d in state.dice]),
                Action(ActionType.ROLL, [d == state.dice[0] for d in state.dice]),
            ]

        for cat in Category:
            if state.score_table.is_available(cat):
                actions.append(Action(ActionType.SELECT_CATEGORY, cat))

        return actions

    # ===============================
    # WYBÓR AKCJI (EPSILON-GREEDY)
    # ===============================
    def choose_action(self, state):
        s = self.encode_state(state)
        actions = self.possible_actions(state)

        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            action = max(
                actions,
                key=lambda a: self.Q[(s, action_key(a))]
            )

        self.last_state = s
        self.last_action = action
        return action

    # ===============================
    # UCZENIE
    # ===============================
    def learn(self, reward, next_state):
        if self.last_state is None:
            return

        s = self.last_state
        a = action_key(self.last_action)
        s2 = self.encode_state(next_state)

        next_actions = self.possible_actions(next_state)

        if not next_actions:
            future = 0
        else:
            future = max(
                self.Q[(s2, action_key(a2))]
                for a2 in next_actions
            )

        self.Q[(s, a)] += self.alpha * (
            reward + self.gamma * future - self.Q[(s, a)]
        )
