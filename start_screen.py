import pygame
import random
import os
from effects import *
from game_logic import GameLogic

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
            base_color="white",
            hovering_color="yellow",
        )
        quit_button = Button(
            image=None,
            pos=(310, 520),
            text_input="exit",
            font=get_font(45),
            base_color="white",
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

        level_manager = Level(self.screen, self.bg_image, self.game_width, self.game_height, self.get_font(30), self.GRAY)

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
            base_color="white",
            hovering_color="green",
        )
        medium_button = Button(
            image=None,
            pos=(345, 470),
            text_input="medium",
            font=get_font(45),
            base_color="white",
            hovering_color="orange",
        )
        hard_button = Button(
            image=None,
            pos=(310, 550),
            text_input="hard",
            font=get_font(45),
            base_color="white",
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

class Level:
    def __init__(self, screen, bg_image, game_width, game_height, font, gray_color):
        self.screen = screen
        self.bg_image = bg_image
        self.game_width = game_width
        self.game_height = game_height
        self.font = font
        self.GRAY = gray_color
        self.memory_pictures = []
        self.rows = 0
        self.cols = 0
        self.num_bombs = 0
        self.num_pairs = 0
        self.pic_size = 0  # Initialize pic_size
        self.padding = 10
        self.left_margin = 0
        self.top_margin = 0
        self.load_memory_pictures()

    def load_memory_pictures(self):
        try:
            self.memory_pictures = [
                os.path.splitext(file)[0]
                for file in os.listdir('Assets/object')
                if file.endswith(('.png', '.jpg', '.jpeg'))
            ]
            print(f"Loaded {len(self.memory_pictures)} memory pictures: {self.memory_pictures}")
        except FileNotFoundError as e:
            print(f"Error loading memory pictures: {e}")
            self.memory_pictures = []

    def setup_game(self, level):
        self.rows, self.cols, self.num_bombs = {
            "easy": (3, 3, 1),
            "medium": (4, 4, 2),
            "hard": (5, 5, 3),
        }[level]

        self.num_pairs = (self.rows * self.cols - self.num_bombs) // 2

        if (self.num_pairs * 2 + self.num_bombs) > (self.rows * self.cols):
            raise ValueError(
                f"Grid size is too small for the number of cards. "
                f"Grid: {self.rows * self.cols}, Required: {self.num_pairs * 2 + self.num_bombs}"
            )

        self.grid_width = self.game_width - 150
        self.grid_height = self.game_height - 150
        self.pic_size = min(self.grid_width // self.cols, self.grid_height // self.rows) - self.padding
        extra_left_offset = 100  # Adjust this value to move the grid more left
        self.left_margin = ((self.game_width - (self.pic_size + self.padding) * self.cols + self.padding) // 2 
                            - extra_left_offset)        
        self.top_margin = (self.game_height - (self.pic_size + self.padding) * self.rows + self.padding) // 2

        # Select images for the game
        selected_images = random.sample(self.memory_pictures, self.num_pairs)
        selected_images *= 2  # Duplicate to make pairs
        selected_images += ["bomb"] * self.num_bombs
        random.shuffle(selected_images)

        # Load and position images
        self.nem_pics = []
        self.nem_pics_rect = []
        self.hidden_images = []

        for item in selected_images:
            picture = pygame.image.load(f'Assets/object/{item}.png')
            picture = pygame.transform.scale(picture, (self.pic_size, self.pic_size))
            self.nem_pics.append(picture)
            picture_rect = picture.get_rect()
            self.nem_pics_rect.append(picture_rect)

        # Set positions of the cards
        for i in range(len(self.nem_pics_rect)):
            self.nem_pics_rect[i][0] = self.left_margin + ((self.pic_size + self.padding) * (i % self.cols))
            self.nem_pics_rect[i][1] = self.top_margin + ((self.pic_size + self.padding) * (i // self.cols))
            self.hidden_images.append(True)

        print(f"Level: {level}, Rows: {self.rows}, Cols: {self.cols}, Bombs: {self.num_bombs}")
        print(f"Number of pairs: {self.num_pairs}, Total cards: {self.rows * self.cols}")
        print(f"Selected images: {selected_images}")


        return self.nem_pics, self.nem_pics_rect, selected_images, self.hidden_images

    print("Game setup complete. Starting game loop...")



    def game_loop(self, selected_images, hidden_images, game_timer):
        """Main game loop."""
        print("Entering game loop...")
        matched_cards = set()  # Keep track of matched cards
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)  # Limit to 30 frames per second
            self.screen.blit(self.bg_image, (0, 0))  # Draw background image

            game_timer.update()
            game_timer.display()

            if game_timer.is_time_up():
                print("Time's up!")
                return
            # Draw all cards (either hidden or revealed)
            for idx, rect in enumerate(self.nem_pics_rect):
                if hidden_images[idx]:
                    pygame.draw.rect(self.screen, self.GRAY, rect)  # Gray rectangle for hidden cards
                else:
                    self.screen.blit(self.nem_pics[idx], rect)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected!")
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(f"Mouse clicked at {event.pos}")
                    for idx, rect in enumerate(self.nem_pics_rect):
                        if not hidden_images[idx] or idx in matched_cards:  # Skip already matched or hidden cards
                            continue
                        if rect.collidepoint(event.pos):  # Check if card was clicked
                            print(f"Card {idx} clicked!")
                            self.flip_card(idx, selected_images, hidden_images, matched_cards)

            # Check if all pairs are matched (excluding bombs)
            if len(matched_cards) == len(selected_images) - self.num_bombs:
                print("You Win!")
                return  # Exit game loop after winning

            pygame.display.update()  # Refresh the screen


    def flip_card(self, idx, selected_images, hidden_images, matched_cards):
        """Flip the selected card and check for matches."""
        print(f"Flipping card {idx}")
        hidden_images[idx] = False

        flipped_cards = [i for i, hidden in enumerate(hidden_images) if not hidden and i != idx]
        print(f"Flipped cards: {flipped_cards}")

        if flipped_cards:
            if selected_images[idx] == selected_images[flipped_cards[0]]:
                print(f"Match found: {selected_images[idx]}")
                matched_cards.add(idx)
                matched_cards.add(flipped_cards[0])
            else:
                print(f"No match: {selected_images[idx]} != {selected_images[flipped_cards[0]]}")
                hidden_images[idx] = True
                hidden_images[flipped_cards[0]] = True