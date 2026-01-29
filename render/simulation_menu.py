import pygame

from ai.random_bot import RandomBot
from ai.greedy_bot import GreedyBot
from ai.heuristic_bot import HeuristicBot
from ai.learning_bot_RL import LearningBotRL
from ai.learning_bot_RL_HEU import LearningBotRL_plus_Heu
from ai.RL_storage import model_exists
from itertools import combinations

class SimulationMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()

        # BOTY
        self.bots = [
            ("RandomBot", RandomBot),
            ("GreedyBot", GreedyBot),
            ("HeuristicBot", HeuristicBot),
        ]

        if model_exists():
            self.bots.append(("RLBot", LearningBotRL_plus_Heu))

        # KOMBINACJE BOTÓW DO SYMULACJI
        self.pairs = []
        for ((name_a, cls_a), (name_b, cls_b)) in combinations(self.bots, 2):
            self.pairs.append((name_a, cls_a, name_b, cls_b))

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        cx = self.screen.get_width() // 2
        y = 110

        for pair in self.pairs:
            rect = pygame.Rect(cx - 220, y, 440, 32)
            self.buttons.append((rect, pair))
            y += 38

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, pair in self.buttons:
                        if rect.collidepoint(event.pos):
                            return pair

            self.draw()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill((240, 240, 240))

        title = self.big_font.render("SYMULACJA – WYBIERZ POJEDYNEK", True, (0, 0, 0))
        self.screen.blit(title, title.get_rect(center=(400, 50)))

        for rect, (a, _, b, _) in self.buttons:
            pygame.draw.rect(self.screen, (200, 200, 200), rect, border_radius=6)
            label = self.font.render(f"{a}  vs  {b}", True, (0, 0, 0))
            self.screen.blit(label, label.get_rect(center=rect.center))

        pygame.display.flip()