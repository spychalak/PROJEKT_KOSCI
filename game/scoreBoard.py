from game.categories import Category


class ScoreTable:

    def __init__(self):
        self.scores = dict.fromkeys(Category, None)

    def is_available(self, category):
        return self.scores[category] is None

    def set_score(self, category, value):
        if not self.is_available(category):
            return False
        self.scores[category] = value
        return True

    def total_score(self):
        return sum(v for v in self.scores.values() if v is not None)
