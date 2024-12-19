import pygame
import random
import os
from effects import *


print("main_menu.py is being loaded")

def main_menu(screen):
    """Main menu screen."""
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(pygame.image.load("Assets/bg/main_menu.png"), (0, 0))  # Background image

        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        play_button = Button(
            image=None,
            pos=(375, 430),
            text_input="new game",
            font=get_font(45),
            base_color=(66, 94, 150),
            hovering_color="yellow",
        )
        quit_button = Button(
            image=None,
            pos=(310, 520),
            text_input="exit",
            font=get_font(45),
            base_color=(66, 94, 150),
            hovering_color="red",
        )

        play_button.changeColor(MAIN_MOUSE_POS)
        play_button.update(screen)
        quit_button.changeColor(MAIN_MOUSE_POS)
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(MAIN_MOUSE_POS):
                    selected_level = difficulty_selection(screen, get_font)  # Get selected level
                    return selected_level  
                if quit_button.checkForInput(MAIN_MOUSE_POS):
                    pygame.quit()
                    exit()
        pygame.display.update()

class MemoryCardGame:
    def __init__(self, game_width=1200, game_height=760, pic_size=128, padding=10, left_margin=75, top_margin=70):
        pygame.init()

        # Game configuration
        self.font = pygame.font.Font("Assets/Pixelicious.ttf", 30)
        self.game_width = int(game_width)
        self.game_height = int(game_height)
        self.pic_size = pic_size
        self.padding = padding
        self.left_margin = left_margin
        self.top_margin = top_margin

        # Colors
        self.WHITE, self.BLACK, self.GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)

        # Screen setup
        self.screen = pygame.display.set_mode((self.game_width, self.game_height))

        # Load assets
        self.load_assets()

    def load_assets(self):
        """Load all required images and assets."""
        game_icon = pygame.image.load('Assets/bg/game_layout.png')
        pygame.display.set_icon(game_icon)

        # Background images
        self.bg_image = pygame.image.load('Assets/bg/game_layout.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.game_width, self.game_height))

        # Bomb image
        self.bomb_image = pygame.image.load(os.path.join('Assets', 'bomb.png'))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.pic_size, self.pic_size))

        # Load memory pictures
        try:
            self.memory_pictures = [os.path.splitext(file)[0] for file in os.listdir('Assets/object') if file.endswith(('.png', '.jpg', '.jpeg'))]
            self.memory_pictures = self.memory_pictures[:13]  # Limit to 13 pairs for consistency
        except FileNotFoundError as e:
            print(f"Error loading memory pictures: {e}")


    def get_font(self, size):
        return pygame.font.Font("Assets/Pixelicious.ttf", size)

    def run(self, selected_level):
        """Main entry point for the game."""
        self.selected_level = selected_level
        selected_level = main_menu(self.screen)

        if not selected_level:
            print("No difficulty selected, exiting.")
            pygame.quit()
            return

        print(f"Starting game at {selected_level} difficulty.")


        try:
            # Set up the game with the selected difficulty
            nem_pics, nem_pics_rect, selected_images, hidden_images = level_manager.setup_game(self.selected_level)
        except ValueError as e:
            print(f"Error: {e}")
            print("Returning to main menu...")
            return  # Return to main menu instead of crashing

        # Start the game loop
        level_manager.game_loop(selected_images, hidden_images)
        print("Game over!")

def difficulty_selection(screen, get_font):
    """Screen for selecting difficulty level."""
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(pygame.image.load("Assets/bg/difficulty_menu.png"), (0, 0))  # Difficulty selection background

        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        easy_button = Button(
            image=None,
            pos=(310, 400),
            text_input="easy",
            font=get_font(45),
            base_color=(66, 94, 150),
            hovering_color="green",
        )
        medium_button = Button(
            image=None,
            pos=(345, 470),
            text_input="medium",
            font=get_font(45),
            base_color=(66, 94, 150),
            hovering_color="orange",
        )
        hard_button = Button(
            image=None,
            pos=(310, 550),
            text_input="hard",
            font=get_font(45),
            base_color=(66, 94, 150),
            hovering_color="red",
        )

        for button in [easy_button, medium_button, hard_button]:
            button.changeColor(MAIN_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.checkForInput(MAIN_MOUSE_POS):
                    return "easy"  # Return difficulty
                if medium_button.checkForInput(MAIN_MOUSE_POS):
                    return "medium"
                if hard_button.checkForInput(MAIN_MOUSE_POS):
                    return "hard"
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
