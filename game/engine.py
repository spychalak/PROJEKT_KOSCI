from game.state import GameState
from game.actions import Action
# from game import rules

class GameEngine:
    def __init__(self):
        self.state = GameState()

    def reset(self):
        self.state = GameState()
        return self.get_observation()

    def step(self, action: Action):
        if self.state.done:
            raise RuntimeError("Gra zakończona – wywołaj reset()")

        reward = 0
        done = False

        if action == Action.ROLL:
            self.state.roll_dice()
            # reward, done = rules.apply_roll_rules(self.state)

       # elif action == Action.SELECT_CATEGORY:
            # reward, done = rules.apply_hold_rules(self.state)

        self.state.done = done
        return self.get_observation(), reward, done

    def get_observation(self):
        return {
            "dice": tuple(self.state.dice),
            "score": self.state.score,
            "round_score": self.state.round_score
        }