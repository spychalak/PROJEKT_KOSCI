from collections import Counter

def detect_pattern(dice):
    counts = Counter(dice)
    values = sorted(counts.values(), reverse=True)
    unique = sorted(set(dice))

    if values[0] >= 4:
        return "FOUR"
    if values[0] == 3 and values[1] == 2:
        return "FULL"
    if values[0] == 3:
        return "TRIPLE"
    if values[0] == 2:
        return "PAIR"

    # strity
    for seq in ([1,2,3,4], [2,3,4,5], [3,4,5,6]):
        if all(x in unique for x in seq):
            return "STRAIGHT_4"
        if sum(1 for x in seq if x in unique) >= 3:
            return "STRAIGHT_3"

    return "NONE"