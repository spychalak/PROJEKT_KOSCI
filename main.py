import pygame

from ai.RL_storage import model_exists, load_model
from ai.learning_bot_RL import LearningBotRL
from ai.learning_bot_RL_HEU import LearningBotRL_plus_Heu
from game.engine import GameEngine
from game.actions import ActionType
from game.scoring import score_category
from render.pygame_ui import PygameUI
from render.menu import MainMenu
from render.bot_menu import BotMenu
from render.train_menu import TrainMenu
from render.simulation_menu import SimulationMenu
from ai.random_bot import RandomBot
from ai.greedy_bot import GreedyBot
from ai.heuristic_bot import HeuristicBot
from train_rl import train_rl
from simulation import simulate_games

SIMULATION_GAMES = 5000
AI_DELAY_MS = 2000


def main():
    while True:
        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Kurnik – Gra w kości")

        # MENU
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

        # TRYBY GRY
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
                train_rl(episodes=5000, resume=False)
            elif choice == "resume":
                train_rl(episodes=5000, resume=True)

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
                ai_bot = LearningBotRL_plus_Heu()
                Q, epsilon, episodes = load_model()
                ai_bot.Q = Q
                ai_bot.epsilon = 0.0
                ai_bot.training = False

            elif bot_choice == "back":
                continue

            engine = GameEngine(players=2)

        elif mode == "sim":
            sim_menu = SimulationMenu(screen)
            choice = sim_menu.run()

            if choice is None:
                continue

            name_a, bot_class_a, name_b, bot_class_b = choice

            pygame.display.iconify()
            simulate_games(bot_class_a, bot_class_b, name_a, name_b, games=SIMULATION_GAMES)
            pygame.display.set_mode((800, 500))
            pygame.display.set_caption("Kurnik – Gra w kości")
            continue

        elif mode == "q":
            return

        else:
            return

        # START GRY
        engine.start_turn()
        ui = PygameUI(engine)

        pending_action = None
        ai_wait_until = 0

        running = True
        while running:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and not (mode == "ai" and engine.current_player == 1)
                    and pending_action is None
                ):
                    ui.handle_click(event.pos)

            # TURA AI
            if (
                mode == "ai"
                and engine.current_player == 1
                and not engine.game_over
            ):
                # FAZA 1 – decyzja
                if pending_action is None:
                    pending_action = ai_bot.choose_action(engine.state)

                    print("\n[AI RUCH]")
                    print("Kości:", engine.state.dice)
                    print("Rzuty pozostałe:", engine.state.rolls_left)
                    print("Akcja:", pending_action.type, pending_action.data)

                    if pending_action.type == ActionType.ROLL:
                        kept = [str(d) for d, k in zip(engine.state.dice, pending_action.data) if k]
                        reroll = [str(d) for d, k in zip(engine.state.dice, pending_action.data) if not k]

                        ui.show_ai_decision([
                            f"Zostawiam: {', '.join(kept) if kept else 'nic'}",
                            f"Losuję: {', '.join(reroll) if reroll else 'nic'}"
                        ])

                    elif pending_action.type == ActionType.SELECT_CATEGORY:
                        ui.show_ai_decision([
                            f"Wybieram kategorię: {pending_action.data.name}",
                            f"Zdobywam {score_category(engine.state.dice, pending_action.data)} punktów"
                        ])

                    ai_wait_until = now + AI_DELAY_MS

                # FAZA 2 – wykonanie po pauzie
                elif now >= ai_wait_until:
                    engine.apply_action(pending_action)
                    pending_action = None
                    ui.clear_ai_decision()

            ui.draw()

            # KONIEC GRY
            if engine.game_over:
                ui.screen.fill((0, 0, 0))
                y = 120

                title = ui.big_font.render("KONIEC GRY", True, (255, 255, 255))
                ui.screen.blit(title, title.get_rect(center=(400, 60)))

                for i, state in enumerate(engine.states):
                    score = state.score_table.total_score()
                    label = f"Gracz {i + 1}"
                    if mode == "ai" and i == 1:
                        label += " (bot)"

                    line = ui.font.render(f"{label}: {score} pkt", True, (255, 255, 255))
                    ui.screen.blit(line, line.get_rect(center=(400, y)))
                    y += 30

                y += 20
                if engine.winner is None:
                    win_text = "REMIS!"
                else:
                    label = f"Gracz {engine.winner + 1}"
                    if mode == "ai" and engine.winner == 1:
                        label += " (bot)"
                    win_text = f"WYGRYWA: {label}"

                win_render = ui.big_font.render(win_text, True, (255, 255, 255))
                ui.screen.blit(win_render, win_render.get_rect(center=(400, y)))

                pygame.display.flip()
                pygame.time.wait(4000)
                running = False

        pygame.quit()


if __name__ == "__main__":
    main()