import pygame
from game.engine import GameEngine
from render.pygame_ui import PygameUI
from render.menu import MainMenu


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Kurnik – Gra w kości")


    # ===== MENU =====
    menu = MainMenu(screen)
    mode = None

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
    elif mode == "ai":
        engine = GameEngine(players=2)  # AI będzie graczem 2
    else:
        return

    engine.start_turn()
    ui = PygameUI(engine)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                ui.handle_click(event.pos)

        ui.draw()

        if engine.game_over:
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
