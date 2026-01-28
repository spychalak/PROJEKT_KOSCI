from collections import Counter
from ai.bot import BaseBot
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category


class HeuristicBot(BaseBot):
    def __init__(self):
        super().__init__("HeuristicBot")

        # 3️⃣ priorytety kategorii (im wcześniej, tym cenniejsza)
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
            Category.CHANCE,
            Category.SIXES,
            Category.FIVES,
            Category.FOURS,
            Category.THREES,
            Category.TWOS,
            Category.ONES,
        ]

    # =====================================================
    # GŁÓWNA DECYZJA
    # =====================================================
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
        return Action(ActionType.SELECT_CATEGORY, cat)

    # =====================================================
    # 1–9: DECYZJA CO TRZYMAĆ
    # =====================================================
    def _choose_dice_to_hold(self, dice, rolls_left, table):
        counts = Counter(dice)
        hold = [False] * 5

        # 9️⃣ jeżeli układ już gotowy i mamy punkty → NIE PSUJEMY
        for cat in self.category_priority:
            if table.is_available(cat) and score_category(dice, cat) > 0:
                return [True] * 5

        # 1️⃣ wykrywanie czwórek / trójek / par
        for value, cnt in counts.items():
            # 4️⃣ >=3 takie same → poluj na czwórkę / generała
            if cnt >= 3:
                return [d == value for d in dice]

        # 6️⃣ dwie pary → poluj na full house
        pairs = [v for v, c in counts.items() if c == 2]
        if len(pairs) == 2 and table.is_available(Category.FULL_HOUSE):
            return [d in pairs for d in dice]

        # 7️⃣ jedna para → zostaw ją i szukaj więcej
        if len(pairs) == 1:
            return [d == pairs[0] for d in dice]

        # 2️⃣ sprawdzanie 4 pod rząd (mały strit)
        unique = sorted(set(dice))
        for straight in ([1, 2, 3, 4],
                         [2, 3, 4, 5],
                         [3, 4, 5, 6]):
            if sum(1 for x in straight if x in unique) >= 4:
                return [d in straight for d in dice]

        # 8️⃣ nic sensownego → zostaw wysokie kości (szansa)
        return [d >= 5 for d in dice]

    # =====================================================
    # 10: WYBÓR KATEGORII (W TYM ZERA)
    # =====================================================
    def _choose_category_for_zero_or_score(self, dice, table):

        # jeśli mamy punktującą kategorię → bierzemy wg priorytetu
        for cat in self.all_category_priority:
            if table.is_available(cat) and score_category(dice, cat) > 0:
                return cat

        # 10️⃣ musimy wpisać ZERO → poświęcamy NAJMNIEJ OPŁACALNE
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

