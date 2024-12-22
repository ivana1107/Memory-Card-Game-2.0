import pygame
import sys
import math

class timer:
    def __init__(self, screen, font, level):
        self.screen = screen
        self.level = level
        self.time_limits = {"easy": 30, "medium": 50, "hard": 80}
        self.start_time = pygame.time.get_ticks()
        self.time_limit = self.time_limits[level]
        self.time_left = self.time_limit
        self.font = pygame.font.Font('Assets/Pixelicious.ttf', 45)

        self.timer_x = 850
        self.timer_y = 140

        # Add sound effect and animation
        self.warning_sound = pygame.mixer.Sound('Assets/warning.mp3')
        self.sound_played = False

        self.shake_offset = 0
        self.shake_speed = 3
        self.shake_intensity = 4

    def update(self):
        # Calculate time left
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_left = max(0, self.time_limit - elapsed_time)

        # Timer warning logic
        if self.time_left <= 6 and not self.sound_played:
            self.warning_sound.play()
            self.sound_played = True
        elif self.time_left > 6:
            self.sound_played = False  # Reset sound if time left is more than 5

    def display(self):
        # Render and display the timer on the top right
        timer_text = self.font.render(f"Time: {int(self.time_left)}s", True, (0, 0, 0))
        text_color = (0, 0, 0)

        # Animation logic
        if self.time_left <= 6:
            text_color = (255, 0, 0)  # Red Text

            # Make text vibrate
            self.shake_offset = int(math.sin(pygame.time.get_ticks() * self.shake_speed) * self.shake_intensity)
            timer_x = self.timer_x + self.shake_offset

            timer_text = self.font.render(f"Time: {int(self.time_left)}s", True, text_color)
        else:
            timer_x = self.timer_x

        self.screen.blit(timer_text, (timer_x, self.timer_y))

    def is_time_up(self):
        # Check if time is up
        return self.time_left <= 0

    def reset(self, level):
        # Resets the timer to its initial state with new time limit based on level
        self.level = level
        self.start_time = pygame.time.get_ticks()
        self.time_limit = self.time_limits[level]  # Update time_limit based on level
        self.time_left = self.time_limit
        self.sound_played = False