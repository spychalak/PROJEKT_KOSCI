from game.categories import Category
from collections import Counter


def score_category(dice, category):
    counts = Counter(dice)
    if category == Category.CHANCE:
        return sum(dice)

    if category == Category.TRIPLE:
        if max(counts.values()) >= 3:
            return sum(dice)
        else:
            return 0

    if category == Category.QUADRUPLE:
        if max(counts.values()) >= 4:
            return sum(dice)
        else:
            return 0

    if category in [
        Category.ONES, Category.TWOS, Category.THREES,
        Category.FOURS, Category.FIVES, Category.SIXES
    ]:
        value = category.value
        return sum(d for d in dice if d == value)

    if category == Category.FULL_HOUSE:
        if sorted(counts.values()) == [2, 3]:
            return 25
        else:
            return 0

    if category == Category.BIG_STRAIGHT:
        straight = sorted(set(dice))
        if straight in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
            return 40
        else:
            return 0
        
    if category == Category.SMALL_STRAIGHT:
        straight = sorted(set(dice))
        if (
                straight[:4] == [1, 2, 3, 4] or
                straight[1:5] == [2, 3, 4, 5] or
                straight[2:6] == [3, 4, 5, 6]
        ):
            return 30
        else:
            return 0

    if category == Category.GENERAL:
        if max(counts.values()) == 5:
            return 50
        else:
            return 0
