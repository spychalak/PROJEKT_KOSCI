import pygame


def show_simulation_result(screen, result):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 28)
    big = pygame.font.SysFont(None, 36)

    y = 80

    title = big.render("WYNIKI SYMULACJI", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(400, 40)))

    lines = [
        f"Liczba gier: {result['games']}",
        "",
        f"Bot A – średnia: {result['avg_a']:.2f}",
        f"Bot B – średnia: {result['avg_b']:.2f}",
        "",
        f"Bot A wygrane: {result['wins_a']} ({100*result['wins_a']/result['games']:.1f}%)",
        f"Bot B wygrane: {result['wins_b']} ({100*result['wins_b']/result['games']:.1f}%)",
        f"Remisy: {result['draws']}",
    ]

    for line in lines:
        txt = font.render(line, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(400, y)))
        y += 28

    pygame.display.flip()