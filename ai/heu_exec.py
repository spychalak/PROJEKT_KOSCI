from collections import Counter
from game.actions import Action, ActionType
from game.categories import Category
from game.scoring import score_category

def hunt_same(dice, n):
    counts = Counter(dice)
    target = max(counts, key=lambda x: counts[x])
    if counts[target] >= n:
        return [d == target for d in dice]
    return [False]*5

def hunt_straight(dice):
    unique = sorted(set(dice))
    for seq in ([1,2,3,4], [2,3,4,5], [3,4,5,6]):
        if sum(1 for x in seq if x in unique) >= 3:
            return [d in seq for d in dice]
    return [False]*5

def best_available_category(state):
    best = None
    best_score = -999

    for cat in Category:
        if not state.score_table.is_available(cat):
            continue

        s = score_category(state.dice, cat)

        # KARA ZA 0 W GÓRNEJ TABELI
        if cat in {
            Category.ONES, Category.TWOS, Category.THREES,
            Category.FOURS, Category.FIVES, Category.SIXES
        } and s == 0:
            s -= 10

        if s > best_score:
            best_score = s
            best = cat

    return best

def worst_available_category(state):
    for cat in [
        Category.ONES, Category.TWOS, Category.THREES,
        Category.FOURS, Category.FIVES, Category.SIXES,
        Category.CHANCE
    ]:
        if state.score_table.is_available(cat):
            return cat
    return best_available_category(state)