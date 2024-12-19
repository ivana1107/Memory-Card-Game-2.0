import pygame
import sys

class timer:
    def __init__(self, screen, font, level):
        self.screen = screen
        self.level = level
        self.time_limits = {"easy": 30, "medium": 50, "hard": 80}
        self.start_time = pygame.time.get_ticks()
        self.time_limit = self.time_limits.get(level, 60)  # Default time limit of 60 seconds
        self.time_left = self.time_limit
        self.font = pygame.font.Font('Assets/Pixelicious.ttf', 45)

        self.timer_x = 850
        self.timer_y = 140

    def update(self):
        # Calculate time left
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_left = max(0, self.time_limit - elapsed_time)

    def display(self):
        # Render and display the timer on the top right
        timer_text = self.font.render(f"Time: {int(self.time_left)}s", True, (0, 0, 0))
        timer_x = self.screen.get_width() - timer_text.get_width() - 20
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def is_time_up(self):
        # Check if time is up
        return self.time_left <= 0
    
    def reset(self):
        """Resets the timer to its initial state."""
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.time_limit  # Reset time_left as well
        self.time_up = False