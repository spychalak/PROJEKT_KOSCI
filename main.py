from game.state import GameState
from game.actions import Action
from game.categories import Category
from game.scoring import score_category


def print_score_table(score_table):
    print("\nTabela wyników:")
    for cat, val in score_table.scores.items():
        status = val if val is not None else "-"
        print(f"{cat.name:15}: {status}")
    print(f"Suma: {score_table.total_score()}\n")

def main():
    state = GameState()
    print("=== Witaj w grze w kości (Kurnik) ===")

    while not state.done:
        state.rolls_left = 3  # reset rzutów na turę
        state.current_round_score = 0
        state.roll_dice(state.dice)
        # Rzuty kośćmi
        while state.rolls_left > 0:
            print(f"\nKości: {state.dice} | Pozostało rzutów: {state.rolls_left}")
            keep_input = input("Podaj indeksy kości do zatrzymania (np. 0 2) lub ENTER dla wszystkich: ")
            keep = [False]*5
            if keep_input.strip():
                for i in map(int, keep_input.strip().split()):
                    if 0 <= i < 5:
                        keep[i] = True

            state.roll_dice(keep)
            print(f"Rzut: {state.dice}")

            reroll = input("Czy chcesz rzucić ponownie? (t/n): ").lower()
            if reroll != "t":
                break

        # Wybór kategorii
        print_score_table(state.score_table)
        available = [cat for cat in Category if state.score_table.is_available(cat)]
        print("Dostępne kategorie:")
        for idx, cat in enumerate(available):
            print(f"{idx}: {cat.name}")

        choice = None
        while choice is None:
            try:
                c = int(input("Wybierz kategorię: "))
                if 0 <= c < len(available):
                    choice = available[c]
            except:
                pass

        points = score_category(state.dice, choice)
        state.score_table.set_score(choice, points)
        print(f"Wybrałeś {choice.name}, zdobywasz {points} punktów")

        # Reset kości
        state.dice = [0]*5

        # Sprawdzenie końca gry
        if all(v is not None for v in state.score_table.scores.values()):
            state.done = True

    print("\n=== KONIEC GRY ===")
    print_score_table(state.score_table)

if __name__ == "__main__":
    main()