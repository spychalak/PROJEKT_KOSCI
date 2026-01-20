import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 52)

        self.options = [
            ("Graj sam", "solo"),
            ("Graj z 2 graczem", "2p"),
            ("Graj z AI", "ai"),
        ]

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        self.buttons.clear()

        button_width = 280
        button_height = 45
        spacing = 65

        # środek pionowy dla CAŁEGO menu
        total_height = len(self.options) * spacing
        start_y = self.screen_rect.centery - total_height // 2 + 30

        for i, (text, mode) in enumerate(self.options):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.centerx = self.screen_rect.centerx
            rect.y = start_y + i * spacing
            self.buttons.append((rect, text, mode))

    def draw(self):
        self.screen.fill((30, 30, 30))

        # ===== TYTUŁ =====
        title = self.big_font.render("KURNIK – GRA W KOŚCI", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_rect.centerx, 120))
        self.screen.blit(title, title_rect)

        # ===== PRZYCISKI =====
        for rect, text, _ in self.buttons:
            pygame.draw.rect(self.screen, (80, 80, 80), rect, border_radius=8)

            label = self.font.render(text, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        for rect, _, mode in self.buttons:
            if rect.collidepoint(pos):
                return mode
        return None