import pygame
from game.categories import Category
from game.scoring import score_category


class PygameUI:
    def __init__(self, engine):
        self.engine = engine
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 32)

        self.dice_rects = []
        self.roll_button_rect = None

        self.held = [False] * 5

        self._create_layout()

    # ===================== LAYOUT =====================

    def _create_layout(self):
        w, h = self.screen_rect.size

        # ===== TABELKA (LEWA STRONA) =====
        self.table_rect = pygame.Rect(0, 0, 300, 440)
        self.table_rect.left = 30
        self.table_rect.centery = self.screen_rect.centery

        # ===== KOŚCI (PRAWA STRONA) =====
        dice_area = pygame.Rect(0, 0, 320, 120)
        dice_area.right = self.screen_rect.right - 30
        dice_area.top = self.table_rect.top + 30

        self.dice_rects.clear()
        spacing = 10
        dice_size = 50

        total_width = 5 * dice_size + 4 * spacing
        start_x = dice_area.centerx - total_width // 2

        for i in range(5):
            rect = pygame.Rect(
                start_x + i * (dice_size + spacing),
                dice_area.centery - dice_size // 2,
                dice_size,
                dice_size
            )
            self.dice_rects.append(rect)

        # ===== ROLL BUTTON =====
        self.roll_button_rect = pygame.Rect(0, 0, 140, 40)
        self.roll_button_rect.centerx = dice_area.centerx
        self.roll_button_rect.top = dice_area.bottom + 30

    # ===================== RYSOWANIE =====================

    def draw(self):
        self.screen.fill((245, 245, 245))

        self._draw_header()
        self._draw_table()
        self._draw_dice()
        self._draw_roll_button()

        pygame.display.flip()

    def _draw_header(self):
        text = self.big_font.render(
            f"Gracz {self.engine.current_player + 1}",
            True,
            (0, 0, 0)
        )
        rect = text.get_rect(center=(self.screen_rect.centerx, 30))
        self.screen.blit(text, rect)

    # ===== TABELKA =====

    def _draw_table(self):
        pygame.draw.rect(self.screen, (220, 220, 220), self.table_rect, border_radius=8)

        state = self.engine.state
        y = self.table_rect.top + 15

        for cat in Category:
            row_rect = pygame.Rect(
                self.table_rect.left + 10,
                y,
                self.table_rect.width - 20,
                26
            )
            y += 2

            # podświetlenie możliwego wyniku
            if state.score_table.is_available(cat):
                preview = score_category(state.dice, cat)
                color = (210, 210, 210)
                pygame.draw.rect(self.screen, color, row_rect)

                val_text = self.font.render(str(preview), True, (0, 0, 180))
            else:
                val = state.score_table.scores[cat]
                val_text = self.font.render(str(val), True, (0, 0, 0))

            name = self.font.render(cat.name, True, (0, 0, 0))
            self.screen.blit(name, (row_rect.left + 5, row_rect.top + 4))
            self.screen.blit(val_text, (row_rect.right - 35, row_rect.top + 4))

            y += 28

        # ===== SUMA =====
        total = state.score_table.total_score()
        total_text = self.font.render(f"Suma: {total}", True, (0, 0, 0))
        self.screen.blit(total_text, (self.table_rect.left + 10, self.table_rect.bottom - 30))

    # ===== KOŚCI =====

    def _draw_dice(self):
        for i, rect in enumerate(self.dice_rects):
            color = (180, 180, 180) if self.held[i] else (255, 255, 255)
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

            val = self.engine.state.dice[i]
            if val > 0:
                text = self.big_font.render(str(val), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

    # ===== ROLL =====

    def _draw_roll_button(self):
        if self.engine.state.rolls_left <= 0:
            return

        pygame.draw.rect(self.screen, (80, 160, 80), self.roll_button_rect, border_radius=8)
        label = self.big_font.render("ROLL", True, (255, 255, 255))
        label_rect = label.get_rect(center=self.roll_button_rect.center)
        self.screen.blit(label, label_rect)

    # ===================== INPUT =====================

    def handle_click(self, pos):
        # ROLL
        if self.roll_button_rect and self.roll_button_rect.collidepoint(pos):
            self.engine.roll(self.held)
            return

        # KOŚCI
        for i, rect in enumerate(self.dice_rects):
            if rect.collidepoint(pos):
                self.held[i] = not self.held[i]
                return

        # TABELKA
        y = self.table_rect.top + 15
        for cat in Category:
            row_rect = pygame.Rect(
                self.table_rect.left + 10,
                y,
                self.table_rect.width - 20,
                26
            )
            y += 2
            if row_rect.collidepoint(pos):
                self.engine.choose_category(cat)
                self.held = [False] * 5
                return
            y += 28