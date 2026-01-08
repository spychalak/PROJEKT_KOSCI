import random
from game.scoreBoard import ScoreTable

class GameState:
    def __init__(self):
        self.dice = [0] * 5           # 5 kości
        self.rolls_left = 3           # ile rzutów pozostało
        self.current_round_score = 0  # punkty w tej turze
        self.score_table = ScoreTable()
        self.done = False

    def roll_dice(self, keep=None):
        """
        Rzuca kośćmi. Nie robi nic, jeśli brak rzutów w turze.
        :param keep: lista 5 booli, True jeśli kość ma być zatrzymana
        """
        if self.rolls_left <= 0:
            return  # brak rzutów → nic nie robimy

        if keep is None:
            keep = [False] * 5  # jeśli nic nie trzymamy, rzucamy wszystkie

        if len(keep) != 5:
            keep = [False] * 5  # niepoprawna długość → traktujemy jak brak trzymania

        new_dice = []
        for i in range(5):
            if keep[i]:
                new_dice.append(self.dice[i])
            else:
                new_dice.append(random.randint(1, 6))
        self.dice = new_dice
        self.rolls_left -= 1
