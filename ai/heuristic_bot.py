from collections import Counter
from ai.bot import BaseBot
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category


class HeuristicBot(BaseBot):
    def __init__(self):
        super().__init__("HeuristicBot")

        # priorytety kategorii (im wcześniej, tym cenniejsza)
        self.category_priority = [
            Category.GENERAL,
            Category.BIG_STRAIGHT,
            Category.FULL_HOUSE,
        ]

        self.all_category_priority = [
            Category.GENERAL,
            Category.BIG_STRAIGHT,
            Category.FULL_HOUSE,
            Category.QUADRUPLE,
            Category.SMALL_STRAIGHT,
            Category.TRIPLE,
            Category.SIXES,
            Category.FIVES,
            Category.FOURS,
            Category.THREES,
            Category.TWOS,
            Category.ONES,
            Category.CHANCE,
        ]

        self.MIN_GOOD_SCORE = {
            Category.ONES: 3,
            Category.TWOS: 6,
            Category.THREES: 9,
            Category.FOURS: 12,
            Category.FIVES: 15,
            Category.SIXES: 18,
            Category.TRIPLE: 15,
            Category.QUADRUPLE: 20,
            Category.CHANCE: 20,
        }

    # WYBÓR CO ROBIMY
    def choose_action(self, state):
        dice = state.dice
        rolls_left = state.rolls_left
        table = state.score_table

        # jeżeli możemy jeszcze rzucać → decyzja co trzymać
        if rolls_left > 0:
            hold = self._choose_dice_to_hold(dice, rolls_left, table)
            return Action(ActionType.ROLL, hold)

        # brak rzutów → wybór kategorii
        cat = self._choose_category_for_zero_or_score(dice, table)

        if cat is None:
            for c, val in table.scores.items():
                if val is None:
                    cat = c
                    break

        return Action(ActionType.SELECT_CATEGORY, cat)

    # INSTRUKCJE
    def _choose_dice_to_hold(self, dice, rolls_left, table):
        counts = Counter(dice)
        hold = [False] * 5

        # jeżeli układ już gotowy i mamy punkty → nie niszczymy go
        for cat in self.category_priority:
            if table.is_available(cat) and score_category(dice, cat) > 0:
                return [True] * 5

        # wykrywanie czwórek / trójek / par
        for value, cnt in counts.items():
            # >=3 takie same → poluj na czwórkę / generała
            if cnt >= 3:

                # jeśli dolna tabela jeszcze otwarta → OK
                if (
                        table.is_available(Category.TRIPLE)
                        or table.is_available(Category.QUADRUPLE)
                        or table.is_available(Category.GENERAL)
                        or self._number_category_available(value, table)
                ):
                    return [d == value for d in dice]



        # dwie pary → poluj na full house
        pairs = [v for v, c in counts.items() if c == 2]
        if len(pairs) == 2 and table.is_available(Category.FULL_HOUSE):
            return [d in pairs for d in dice]

        # jedna para → zostaw ją i szukaj więcej
        if len(pairs) == 1:
            val = pairs[0]

            # trzymaj tylko jeśli są jeszcze sensowne kategorie dostępne
            if self._number_category_available(val, table):
                return [d == val for d in dice]



        # sprawdzanie 4 pod rząd (mały strit)
        unique = sorted(set(dice))
        for straight in ([1, 2, 3, 4],
                         [2, 3, 4, 5],
                         [3, 4, 5, 6]):
            if sum(1 for x in straight if x in unique) >= 4:
                return [d in straight for d in dice]

        upper_left = self._upper_categories_left(table)

        lower_open = any([
            table.is_available(Category.TRIPLE),
            table.is_available(Category.QUADRUPLE),
            table.is_available(Category.FULL_HOUSE),
            table.is_available(Category.CHANCE),
        ])

        if not lower_open and len(upper_left) <= 4:

            counts = Counter(dice)

            # znajdź najwyższą sensowną kość
            best_value = None

            for val in sorted(counts.keys(), reverse=True):

                if self._number_category_available(val, table):
                    best_value = val
                    break

            if best_value is not None:
                return [d == best_value for d in dice]

        # nic sensownego → zostaw wysokie kości (szansa)
        high_target = 6 if table.is_available(Category.SIXES) else 5
        return [d >= high_target for d in dice]

    # 10: WYBÓR KATEGORII (W TYM ZERA)
    def _choose_category_for_zero_or_score(self, dice, table):

        if table.is_available(Category.GENERAL) and score_category(dice, Category.GENERAL) > 0:
            return Category.GENERAL

        if table.is_available(Category.QUADRUPLE) and score_category(dice, Category.QUADRUPLE) > 0:
            return Category.QUADRUPLE

        # jeśli mamy punktującą kategorię → bierzemy wg priorytetu
        for cat in self.all_category_priority:
            if table.is_available(cat):
                score = score_category(dice, cat)

                if score >= self.MIN_GOOD_SCORE.get(cat, 1):
                    return cat

        # musimy wpisać ZERO → poświęcamy najmniej opłacalne
        zero_priority = [
            Category.ONES,
            Category.TWOS,
            Category.THREES,
            Category.FOURS,
            Category.CHANCE,
            Category.SMALL_STRAIGHT,
            Category.TRIPLE,
            Category.FULL_HOUSE,
            Category.QUADRUPLE,
            Category.BIG_STRAIGHT,
            Category.GENERAL,
        ]

        for cat in zero_priority:
            if table.is_available(cat):
                return cat

    def _number_category_available(self, value, table):
        mapping = {
            1: Category.ONES,
            2: Category.TWOS,
            3: Category.THREES,
            4: Category.FOURS,
            5: Category.FIVES,
            6: Category.SIXES,
        }
        return table.is_available(mapping[value])

    def _upper_categories_left(self, table):
        upper = [
            Category.ONES,
            Category.TWOS,
            Category.THREES,
            Category.FOURS,
            Category.FIVES,
            Category.SIXES,
        ]

        return [cat for cat in upper if table.is_available(cat)]