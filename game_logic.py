import pygame
import random
import time
from timer import timer

class GameLogic:
    def __init__(self, screen, difficulty, assets):
        self.screen = screen
        if difficulty is None:
            difficulty = "easy"
        self.difficulty = difficulty
        self.assets = assets
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.bomb_indices = []
        self.bomb_shuffled = False
        self.game_timer = timer(
            screen, pygame.font.Font("Assets/Pixelicious.ttf", 45), difficulty
        )

        self.card_rects = []  # Store card rects
        self.left_margin = 0
        self.top_margin = self.assets["top_margin"]

        # Keep track of time when cards are flipped
        self.flip_time = 0

        # Animation parameters
        self.card_animation_duration = 1000  # Duration of shuffle animation in milliseconds
        self.shuffle_start_time = None  # Timestamp when shuffle starts
        self.shuffle_animating = False  # Flag to control the animation

    def get_level_config(self):
        if self.difficulty == "easy":
            return 3, 3, 1
        elif self.difficulty == "medium":
            return 4, 4, 2
        elif self.difficulty == "hard":
            return 5, 5, 3

    def load_cards(self):
        self.rows, self.cols, self.num_bombs = self.get_level_config()
        # Get game_width from screen
        game_width = self.screen.get_width()
        game_height = self.screen.get_height()

        # Calculate horizontal and vertical centering
        board_width = (
            self.cols * (self.assets["pic_size"] + self.assets["padding"])
            - self.assets["padding"]
        )
        board_height = (
            self.rows * (self.assets["pic_size"] + self.assets["padding"])
            - self.assets["padding"]
        )

        # Adjust left_margin to be closer to the left edge
        self.left_margin = (game_width - board_width) // 4  # Reduced to //4 to shift left
        self.top_margin = (game_height - board_height) // 2  # Center vertically

        # Select images for pairs and bomb
        num_pairs = (self.rows * self.cols - self.num_bombs) // 2
        images = random.sample(self.assets["memory_pictures"], num_pairs)
        images *= 2  # Duplicate images to form pairs
        images += ["bomb"] * self.num_bombs
        random.shuffle(images)
        self.cards = images
        self.bomb_indices = [i for i, card in enumerate(self.cards) if card == "bomb"]

        # Calculate and store card rectangles
        self.card_rects = []
        for idx in range(len(self.cards)):
            x = idx % self.cols
            y = idx // self.cols
            pos_x = (
                x * (self.assets["pic_size"] + self.assets["padding"])
                + self.left_margin
            )
            pos_y = (
                y * (self.assets["pic_size"] + self.assets["padding"])
                + self.top_margin
            )
            rect = pygame.Rect(
                pos_x, pos_y, self.assets["pic_size"], self.assets["pic_size"]
            )
            self.card_rects.append(rect)

    def start_shuffle(self):
    # Initialize new_card_positions with target positions
        self.new_card_positions = []
        for idx, rect in enumerate(self.card_rects):
        # Store the final target position for each card in self.new_card_positions
            target_x = random.randint(self.left_margin, self.screen.get_width() - self.assets["pic_size"])
            target_y = random.randint(self.top_margin, self.screen.get_height() - self.assets["pic_size"])
            self.new_card_positions.append((target_x, target_y))

    def animate_shuffle(self, current_time):
    # Initialize shuffle_start_time if shuffle is starting
        if self.shuffle_animating and not hasattr(self, 'shuffle_start_time'):
            self.shuffle_start_time = current_time
        print(f"shuffle_start_time initialized at {self.shuffle_start_time}")
    
        if self.shuffle_animating:
        # Ensure shuffle_start_time is not None before calculating elapsed time
            if self.shuffle_start_time is not None:
                elapsed_time = current_time - self.shuffle_start_time
            
            if elapsed_time < self.card_animation_duration:
                # Calculate progress of animation (0 to 1)
                progress = elapsed_time / self.card_animation_duration
                
                # Ensure both lists have the same length
                if len(self.new_card_positions) == len(self.card_rects):
                    # Update the card positions based on animation progress
                    for i, rect in enumerate(self.card_rects):
                        x_offset = self.new_card_positions[i][0] - rect.x
                        y_offset = self.new_card_positions[i][1] - rect.y
                        rect.x += int(x_offset * progress)
                        rect.y += int(y_offset * progress)
                else:
                    print(f"ERROR: The lengths of new_card_positions ({len(self.new_card_positions)}) and card_rects ({len(self.card_rects)}) do not match!")
            else:
                # Once animation is done, snap the cards to final positions
                for i, rect in enumerate(self.card_rects):
                    rect.x = self.new_card_positions[i][0]
                    rect.y = self.new_card_positions[i][1]
                self.shuffle_animating = False
                # Reset shuffle_start_time once animation is done
                del self.shuffle_start_time
        else:
            # Print a message if shuffle_start_time is None unexpectedly
            print("ERROR: shuffle_start_time is None!")


    def shuffle_unmatched_cards(self):
        unmatched_indices = [
        i for i in range(len(self.cards)) if i not in self.matched_cards and i not in self.bomb_indices
    ]

        if unmatched_indices:
        # Generate a derangement of unmatched cards
            shuffled_cards = [self.cards[i] for i in unmatched_indices]
            while True:
                random.shuffle(shuffled_cards)
                if all(shuffled_cards[i] != self.cards[unmatched_indices[i]] for i in range(len(unmatched_indices))):
                    break

        # Store the new positions for the animation
        self.new_card_positions = []
        for i, idx in enumerate(unmatched_indices):
            x = idx % self.cols
            y = idx // self.cols
            pos_x = (
                x * (self.assets["pic_size"] + self.assets["padding"])
                + self.left_margin
            )
            pos_y = (
                y * (self.assets["pic_size"] + self.assets["padding"])
                + self.top_margin
            )
            self.new_card_positions.append((pos_x, pos_y))

        # Start the animation
        self.shuffle_start_time = pygame.time.get_ticks()
        self.shuffle_animating = True

        # Update the self.cards list with the shuffled values at the correct indices
        for i, idx in enumerate(unmatched_indices):
            self.cards[idx] = shuffled_cards[i]

    def draw_board(self):
        # Animate the card shuffle
        current_time = pygame.time.get_ticks()
        self.animate_shuffle(current_time)

        # Draw the game board
        for idx, card in enumerate(self.cards):
            rect = self.card_rects[idx]  # Use stored rect

            if idx in self.flipped_cards or idx in self.matched_cards:
                if card == "bomb":
                    self.screen.blit(self.assets["bomb_image"], rect)
                else:
                    image = pygame.image.load(f"Assets/object/{card}.png")
                    image = pygame.transform.scale(
                        image, (self.assets["pic_size"], self.assets["pic_size"])
                    )
                    self.screen.blit(image, rect)
            else:
                # Draw card back image instead of gray rectangle
                self.screen.blit(self.card_back, rect)

    def check_match(self):
        if len(self.flipped_cards) == 2:
            idx1, idx2 = self.flipped_cards
            card1, card2 = self.cards[idx1], self.cards[idx2]

            if card1 == "bomb" or card2 == "bomb":
                # Bomb triggered: Keep bomb open and shuffle unmatched cards
                if not self.bomb_shuffled:
                    self.shuffle_unmatched_cards()
                    self.bomb_shuffled = True

                # Update matched_cards and clear flipped_cards after bomb
                # Only add the bomb to matched_cards
                bomb_idx = idx1 if card1 == "bomb" else idx2
                self.matched_cards.add(bomb_idx)

                self.flipped_cards = []
                self.flip_time = 0
            elif card1 == card2:
                # Match found: Keep cards open
                self.matched_cards.update(self.flipped_cards)
                self.flipped_cards = []
            else:
                # Unmatched cards: Flip back after a delay
                current_time = pygame.time.get_ticks()
                if current_time - self.flip_time > 1000:  # Check if 1 second has passed
                    self.flipped_cards = []
                    self.flip_time = 0  # Reset the timer
        elif len(self.flipped_cards) == 1:
            self.flip_time = pygame.time.get_ticks()

    def handle_click(self, pos):
        # Use stored rects for collision detection
        for idx, rect in enumerate(self.card_rects):
            if (
                rect.collidepoint(pos)
                and idx not in self.flipped_cards
                and idx not in self.matched_cards
            ):
                if len(self.flipped_cards) < 2:
                    self.flipped_cards.append(idx)
                    
                    # Reset bomb_shuffled if a non-bomb card is clicked
                    if len(self.flipped_cards) == 1:
                        card_idx = self.flipped_cards[0]
                        if self.cards[card_idx] != "bomb":
                            self.bomb_shuffled = False
                break

    def game_loop(self):
        self.load_cards()  # Now load_cards can access game_width from screen
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.assets["bg_image"], (0, 0))
            self.draw_board()

            self.game_timer.update()
            self.game_timer.display()

            if self.game_timer.is_time_up():
                return "lose"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.check_match()

            # Win condition: Check if all cards are matched
            if len(self.matched_cards) == len(self.cards):
                return "win"

            pygame.display.update()

    def reset_game(self):
        """Resets the game state for a new game."""
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.bomb_indices = []
        self.bomb_shuffled = False
        self.card_rects = []
        self.flip_time = 0
        self.game_timer.reset()  # Assuming you have a reset method in your timer class
        self.load_cards()

    def load_assets(self):
        # Load card back image
        self.card_back = pygame.image.load("Assets/card_back.png")
        self.card_back = pygame.transform.scale(self.card_back, (self.assets["pic_size"], self.assets["pic_size"]))

    def draw_board(self):
        # Animate the card shuffle
        current_time = pygame.time.get_ticks()
        self.animate_shuffle(current_time)

        # Draw the game board
        for idx, card in enumerate(self.cards):
            rect = self.card_rects[idx]  # Use stored rect

            if idx in self.flipped_cards or idx in self.matched_cards:
                if card == "bomb":
                    self.screen.blit(self.assets["bomb_image"], rect)
                else:
                    image = pygame.image.load(f"Assets/object/{card}.png")
                    image = pygame.transform.scale(
                        image, (self.assets["pic_size"], self.assets["pic_size"])
                    )
                    self.screen.blit(image, rect)
            else:
                # Draw card back image instead of gray rectangle
                self.screen.blit(self.card_back, rect)

    def reset_game(self):
        """Resets the game state for a new game.""" 
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.bomb_indices = []
        self.bomb_shuffled = False
        self.card_rects = []
        self.flip_time = 0
        self.game_timer.reset()
        self.load_assets()  # Load the card back image
        self.load_cards()
