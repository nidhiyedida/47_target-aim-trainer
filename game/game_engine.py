import pygame
import random
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.target = self._spawn_target()

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.game_over_detail_font = pygame.font.SysFont("Arial", 28)
        self.game_over_message_font = pygame.font.SysFont("Arial", 22)
        self.game_over = False

    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - self.margin)
        return Target(x, y)

    def handle_event(self, event):
        if self.game_over:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.target = self._spawn_target()
        else:
            self.misses += 1

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if self.game_over:
            title = self.game_over_font.render("GAME OVER", True, WHITE)
            score = self.game_over_detail_font.render(
                f"Final Score: {self.score}", True, WHITE
            )
            accuracy = self.game_over_detail_font.render(
                f"Final Accuracy: {self.accuracy()}%", True, WHITE
            )
            message = self.game_over_message_font.render(
                "Close the window to exit.", True, WHITE
            )

            screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 90)))
            screen.blit(score, score.get_rect(center=(self.width // 2, self.height // 2 - 20)))
            screen.blit(accuracy, accuracy.get_rect(center=(self.width // 2, self.height // 2 + 25)))
            screen.blit(message, message.get_rect(center=(self.width // 2, self.height // 2 + 95)))
            return

        r = int(self.target.visual_radius())
        pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
        pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))
