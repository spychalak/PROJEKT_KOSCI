from abc import ABC, abstractmethod
from game.actions import Action, ActionType


class BaseBot(ABC):
    def __init__(self, name="Bot"):
        self.name = name

    @abstractmethod
    def choose_action(self, game_state) -> Action:
        """
        Zwraca Action na podstawie aktualnego GameState
        """
        pass