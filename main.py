import pygame

from ai.RL_storage import model_exists, load_model
from ai.learning_bot_RL import LearningBotRL
from game.engine import GameEngine
from render.pygame_ui import PygameUI
from render.menu import MainMenu
from render.bot_menu import BotMenu
from render.train_menu import TrainMenu
from ai.random_bot import RandomBot
from ai.greedy_bot import GreedyBot
from ai.heuristic_bot import HeuristicBot
from train_rl import train_rl

def main():
    while(True):
        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Kurnik – Gra w kości")


        # ===== MENU =====
        menu = MainMenu(screen)
        mode = None
        ai_bot = None

        while mode is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mode = menu.handle_click(event.pos)

            menu.draw()

        # ===== START GRY =====
        if mode == "solo":
            engine = GameEngine(players=1)
        elif mode == "2p":
            engine = GameEngine(players=2)
        elif mode == "train":
            train_menu = TrainMenu(screen)
            choice = None

            while choice is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        choice = train_menu.handle_click(event.pos)

                train_menu.draw()

            pygame.display.iconify()

            if choice == "new":
                train_rl(episodes=3000, resume=False)
            elif choice == "resume":
                train_rl(episodes=3000, resume=True)

            pygame.display.set_mode((800, 500))
            pygame.display.set_caption("Kurnik – Gra w kości")
            continue
        elif mode == "ai":
            bot_menu = BotMenu(screen)
            bot_choice = None
            while bot_choice is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bot_choice = bot_menu.handle_click(event.pos)

                bot_menu.draw()
            if bot_choice == "random":
                ai_bot = RandomBot()
            elif bot_choice == "greedy":
                ai_bot = GreedyBot()
            elif bot_choice == "heuristic":
                ai_bot = HeuristicBot()
            elif bot_choice == "rl":
                if not model_exists():
                    print("Brak wytrenowanego modelu RL")
                    continue
                ai_bot = LearningBotRL()
                Q, epsilon, episodes = load_model()
                ai_bot.Q = Q
                ai_bot.epsilon = 0.0  # ❗ zero eksploracji w pygame
                ai_bot.training = False
            elif bot_choice == "back":
                continue
            engine = GameEngine(players=2)  # AI będzie graczem 2
        elif mode == "q":
            return 0
        else:
            return

        engine.start_turn()
        ui = PygameUI(engine)

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # człowiek klika tylko gdy to NIE tura AI
                if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and not (mode == "ai" and engine.current_player == 1)
                ):
                    ui.handle_click(event.pos)

                # ===== TURA AI =====
            if mode == "ai" and engine.current_player == 1 and not engine.game_over:
                prev_score = engine.state.score_table.total_score()

                action = ai_bot.choose_action(engine.state)

                print("\n[AI RUCH]")
                print("Kości:", engine.state.dice)
                print("Rzuty pozostałe:", engine.state.rolls_left)
                print("Akcja:", action.type, action.data)

                engine.apply_action(action)

                new_score = engine.state.score_table.total_score()
                reward = new_score - prev_score

                if hasattr(ai_bot, "learn"):
                    ai_bot.learn(reward, engine.state)

                # 👉 NAJWAŻNIEJSZE
                ui.draw()
                pygame.display.flip()
                pygame.time.wait(2500)  # pauza po ruchu AI

                continue

            ui.draw()

            if engine.game_over:
                if mode == "ai" and hasattr(ai_bot, "learn"):
                    if engine.winner == 1:
                        ai_bot.learn(50, engine.state)
                    else:
                        ai_bot.learn(-10, engine.state)

                ui.screen.fill((0, 0, 0))
                if engine.winner is None:
                    text = ui.big_font.render("REMIS!", True, (255, 255, 255))
                else:
                    text = ui.big_font.render(
                        f"WYGRYWA GRACZ {engine.winner + 1}!",
                        True,
                        (255, 255, 255)
                    )
                ui.screen.blit(text, (300, 300))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

        pygame.quit()


if __name__ == "__main__":
    main()
