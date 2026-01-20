from game.state import GameState
from game.categories import Category
from game.scoring import score_category


class GameEngine:
    def __init__(self, players=2):
        self.players = players
        self.states = [GameState() for _ in range(players)]
        self.current_player = 0

        self.game_over = False
        self.winner = None

    # ===================== TURA =====================

    @property
    def state(self):
        """Aktualny GameState (dla UI)"""
        return self.states[self.current_player]

    def start_turn(self):
        state = self.state
        state.rolls_left = 3
        state.dice = [0] * 5

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.players
        self.start_turn()

    # ===================== AKCJE =====================

    def roll(self, keep_mask):
        """
        keep_mask: lista 5 booli
        """
        if self.game_over:
            return

        state = self.state

        if state.rolls_left <= 0:
            return

        state.roll_dice(keep_mask)

    def choose_category(self, category: Category):
        """
        Wybór kategorii kończy turę
        """
        if self.game_over:
            return

        state = self.state

        # kategoria zajęta → ignorujemy klik
        if not state.score_table.is_available(category):
            return

        # liczenie punktów
        points = score_category(state.dice, category)
        state.score_table.set_score(category, points)

        # sprawdzamy koniec gry
        if self._check_game_over():
            self.game_over = True
            self._set_winner()
            return

        # następny gracz
        self.next_player()

    # ===================== KONIEC GRY =====================

    def _check_game_over(self):
        """
        Gra kończy się, gdy WSZYSCY gracze mają zapełnione tabele
        """
        for state in self.states:
            if not all(v is not None for v in state.score_table.scores.values()):
                return False
        return True

    def _set_winner(self):
        scores = [state.score_table.total_score() for state in self.states]
        max_score = max(scores)

        # remis → winner = None
        if scores.count(max_score) > 1:
            self.winner = None
        else:
            self.winner = scores.index(max_score)

    # ===================== DEBUG / INFO =====================

    def get_scores(self):
        return [state.score_table.total_score() for state in self.states]