import pygame


class BotMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 48)

        w, h = screen.get_size()
        cx = w // 2

        self.buttons = {
            "random": pygame.Rect(cx - 120, 180, 240, 40),
            "greedy": pygame.Rect(cx - 120, 240, 240, 40),
            # "learning": pygame.Rect(cx - 120, 300, 240, 40),
            "back": pygame.Rect(cx - 120, 360, 240, 40),
        }

    def draw(self):
        self.screen.fill((30, 30, 30))

        title = self.title_font.render("Wybierz bota", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title, title_rect)

        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            label = self.font.render(name.upper(), True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return name
        return None