from game.engine import GameEngine


def simulate_games(bot_a, bot_b, name_a, name_b, games):
    print("\n")
    print("START SYMULACJI")
    print(f"{name_a}  vs  {name_b}")
    print(f"Liczba gier: {games}")
    print("\n")

    wins = [0, 0]
    scores_a = []
    scores_b = []

    for g in range(games):
        engine = GameEngine(players=2)
        engine.start_turn()

        bots = [bot_a(), bot_b()]

        bot_A = bot_a()
        bot_B = bot_b()

        if hasattr(bot_A, "epsilon"):
            bot_A.epsilon = 0.0

        if hasattr(bot_B, "epsilon"):
            bot_B.epsilon = 0.0

        while not engine.game_over:
            current = engine.current_player
            action = bots[current].choose_action(engine.state)
            engine.apply_action(action)

        s0, s1 = engine.get_scores()
        scores_a.append(s0)
        scores_b.append(s1)

        if s0 > s1:
            wins[0] += 1
        elif s1 > s0:
            wins[1] += 1

        if g % max(1, games // 10) == 0:
            print(f"[SYMULACJA] {g}/{games}")

    avg_a = sum(scores_a) / games
    avg_b = sum(scores_b) / games

    print("\n")
    print("KONIEC SYMULACJI")
    print(f"{name_a} wygrane: {wins[0]} ({wins[0]/games*100:.1f}%)")
    print(f"{name_b} wygrane: {wins[1]} ({wins[1]/games*100:.1f}%)")
    print(f"Remisy: {games - wins[0] - wins[1]}")
    print(f"Średni wynik {name_a}: {avg_a:.2f}")
    print(f"Średni wynik {name_b}: {avg_b:.2f}")
    print("\n")
