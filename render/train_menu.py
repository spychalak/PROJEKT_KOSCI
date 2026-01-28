import pygame
from ai.RL_storage import model_exists


class TrainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title = pygame.font.SysFont(None, 48)

        w, _ = screen.get_size()
        cx = w // 2

        self.buttons = {
            "new": pygame.Rect(cx - 140, 200, 280, 40),
            "resume": pygame.Rect(cx - 140, 260, 280, 40),
            "back": pygame.Rect(cx - 140, 320, 280, 40),
        }

    def draw(self):
        self.screen.fill((30, 30, 30))

        t = self.title.render("Trenuj AI", True, (255, 255, 255))
        self.screen.blit(t, t.get_rect(center=(400, 130)))

        for key, rect in self.buttons.items():
            if key == "resume" and not model_exists():
                pygame.draw.rect(self.screen, (120, 120, 120), rect)
            else:
                pygame.draw.rect(self.screen, (200, 200, 200), rect)

            label = self.font.render(key.upper(), True, (0, 0, 0))
            self.screen.blit(label, label.get_rect(center=rect.center))

        pygame.display.flip()

    def handle_click(self, pos):
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if key == "resume" and not model_exists():
                    return None
                return key
        return None