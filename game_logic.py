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
        self.tap_sound = pygame.mixer.Sound("Assets/tap.wav")

        self.card_rects = []  # Store card rects
        self.left_margin = 0
        self.top_margin = self.assets["top_margin"]

        # Keep track of time when cards are flipped
        self.flip_time = 0

        # Animation parameters
        self.card_animation_duration = 500  # Duration of shuffle animation in milliseconds, made shorter
        self.shuffle_start_time = None  # Timestamp when shuffle starts
        self.shuffle_animating = False  # Flag to control the animation
        self.original_card_positions = []
        self.new_card_positions = []

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
        self.left_margin = (game_width - board_width) // 4  
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

    def start_shuffle_animation(self):
        # Initialize card positions for animation
        self.original_card_positions = [rect.topleft for rect in self.card_rects]
        self.new_card_positions = []

        # Get the indices of unmatched and non-bomb cards
        unmatched_non_bomb_indices = [i for i in range(len(self.cards)) if i not in self.matched_cards and i not in self.bomb_indices]

        # Create a list of positions for unmatched cards
        unmatched_card_positions = [self.original_card_positions[i] for i in unmatched_non_bomb_indices]

        # Shuffle these positions
        random.shuffle(unmatched_card_positions)

        # Assign the shuffled positions to new_card_positions
        for pos in unmatched_card_positions:
            self.new_card_positions.append(pos)

        # Set the animation flag and start time
        self.shuffle_animating = True
        self.shuffle_start_time = pygame.time.get_ticks()

    def animate_shuffle(self, current_time):
        if self.shuffle_animating:
            if self.shuffle_start_time is not None:
                elapsed_time = current_time - self.shuffle_start_time
            else:
                elapsed_time = 0

            if elapsed_time >= self.card_animation_duration:
                # Animation is finished
                self.shuffle_animating = False
                self.shuffle_start_time = None

                # Make sure card positions are updated correctly after animation
                unmatched_non_bomb_indices = [i for i in range(len(self.cards)) if i not in self.matched_cards and i not in self.bomb_indices]
                for i, idx in enumerate(unmatched_non_bomb_indices):
                    self.card_rects[idx].topleft = self.new_card_positions[i]
                return

            # Calculate animation progress
            progress = elapsed_time / self.card_animation_duration

            # Animate only unmatched and non-bomb cards
            unmatched_non_bomb_indices = [i for i in range(len(self.cards)) if i not in self.matched_cards and i not in self.bomb_indices]
            for i, idx in enumerate(unmatched_non_bomb_indices):
                rect = self.card_rects[idx]
                target_pos = self.new_card_positions[i]
                original_pos = self.original_card_positions[idx]
                rect.x = int(original_pos[0] + (target_pos[0] - original_pos[0]) * progress)
                rect.y = int(original_pos[1] + (target_pos[1] - original_pos[1]) * progress)

    def shuffle_unmatched_cards(self):
        # Identify unmatched and non-bomb cards
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

            # Update the self.cards list with the shuffled values at the correct indices
            for i, idx in enumerate(unmatched_indices):
                self.cards[idx] = shuffled_cards[i]
        
        # Start the shuffle animation
        self.start_shuffle_animation()

    def draw_rounded_rect(self, rect, color, radius):
        # Draw a rounded rectangle
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        return self.screen.blit(rectangle, pos)

    def draw_card_back(self, rect):
        # Draw the card back with rounded corners
        border_radius = 10
        self.draw_rounded_rect(rect, (200, 200, 200), border_radius) 
        self.screen.blit(self.card_back, rect)

    def draw_card_face(self, rect, card):
        # Draw the card face (image) without rounded corners
        if card == "bomb":
            image = self.assets["bomb_image"]
        else:
            image = pygame.image.load(f"Assets/object/{card}.png")
        image = pygame.transform.scale(image, (self.assets["pic_size"], self.assets["pic_size"]))
        self.screen.blit(image, rect)

    def draw_board(self):
        # Animate the card shuffle
        current_time = pygame.time.get_ticks()
        self.animate_shuffle(current_time)

        # Draw the game board
        for idx, card in enumerate(self.cards):
            rect = self.card_rects[idx]

            if idx in self.flipped_cards or idx in self.matched_cards:
                # Draw face-up card
                self.draw_card_face(rect, card)
            else:
                # Draw face-down card (card back)
                self.draw_card_back(rect)

    def check_match(self):
        if len(self.flipped_cards) == 2:
            idx1, idx2 = self.flipped_cards
            card1, card2 = self.cards[idx1], self.cards[idx2]

            if card1 == "bomb" or card2 == "bomb":
                # Bomb triggered: Keep bomb open and shuffle unmatched cards
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
        # Play tap sound when a card is clicked
        self.tap_sound.play()
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
        self.load_assets()
        self.load_cards()
        clock = pygame.time.Clock()

        # Load and play background music
        pygame.mixer.music.load('Assets/star.mp3')
        pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
        pygame.mixer.music.play(-1)  # Play in a loop

        while True:
            clock.tick(30)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.assets["bg_image"], (0, 0))
            self.draw_board()

            self.game_timer.update()
            self.game_timer.display()

            if self.game_timer.is_time_up():
                pygame.mixer.music.stop()
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
                pygame.mixer.music.stop()
                return "win"

            pygame.display.update()

    def reset_game(self):
        # Resets the game state for a new game
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.bomb_indices = []
        self.bomb_shuffled = False
        self.card_rects = []
        self.flip_time = 0
        self.game_timer.reset(self.difficulty)  # Pass the difficulty level to reset
        self.shuffle_animating = False  # Reset animation flag
        self.shuffle_start_time = None
        self.new_card_positions = []
        self.original_card_positions = []
        self.load_cards()

    def load_assets(self):
        # Load card back image
        self.card_back = pygame.image.load("Assets/card_back.png")
        self.card_back = pygame.transform.scale(self.card_back, (self.assets["pic_size"], self.assets["pic_size"]))

    def card_click(self, card_x, card_y):
        self.tap_sound.play()