from ai.learning_bot_RL_HEU import LearningBotRL_plus_Heu
from game.engine import GameEngine
from ai.learning_bot_RL import LearningBotRL
from ai.RL_storage import save_model, load_model, model_exists
import time


def train_rl(episodes, resume=False):
    print("\n=== TRENING RL ===\n")

    if resume and model_exists():
        Q, epsilon, done = load_model()
        bot = LearningBotRL_plus_Heu()
        bot.Q = Q
        start_episode = done
        print(f"Kontynuacja treningu od epizodu {done}")
    else:
        bot = LearningBotRL_plus_Heu()
        start_episode = 0
        print("Nowy trening")

    bot.training = True
    start_time = time.time()

    for ep in range(start_episode, start_episode + episodes):
        engine = GameEngine(players=1)
        engine.start_turn()

        while not engine.game_over:
            prev_score = engine.state.score_table.total_score()
            action = bot.choose_action(engine.state)
            engine.apply_action(action)
            reward = engine.state.score_table.total_score() - prev_score
            bot.learn(reward, engine.state)

        bot.learn(50, engine.state)

        print(len(bot.Q))
        bot.end_episode()

        if ep % 100 == 0:
            elapsed = time.time() - start_time
            print(f"[TRAIN] ep={ep} eps={bot.epsilon:.3f} time={elapsed:.1f}s")

    save_model(bot.Q, bot.epsilon, start_episode + episodes)

    print("\nTRENING ZAKOŃCZONY")
    print(f"Zapisano epizody: {start_episode + episodes}")