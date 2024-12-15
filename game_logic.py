import pygame
import random
import time

class GameLogic:
    def __init__(self, screen, difficulty, assets, font):
        self.screen = screen
        self.difficulty = difficulty
        self.assets = assets
        self.font = font
        self.rows, self.cols, self.num_bombs = self.get_level_config()
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.start_time = time.time()
        self.time_limit = 60  # seconds

    def get_level_config(self):
        if self.difficulty == "easy":
            return 3, 3, 1
        elif self.difficulty == "medium":
            return 4, 4, 2
        elif self.difficulty == "hard":
            return 5, 5, 4

    def load_cards(self):
        # Select images for pairs and bomb
        num_pairs = (self.rows * self.cols - self.num_bombs) // 2
        images = random.sample(self.assets['memory_pictures'], num_pairs)
        images *= 2  # Duplicate images to form pairs
        images += ['bomb'] * self.num_bombs
        random.shuffle(images)
        self.cards = images

    def draw_board(self):
        # Draw the game board
        for idx, card in enumerate(self.cards):
            x = idx % self.cols
            y = idx // self.cols
            pos_x = x * (self.assets['pic_size'] + self.assets['padding']) + self.assets['left_margin']
            pos_y = y * (self.assets['pic_size'] + self.assets['padding']) + self.assets['top_margin']
            rect = pygame.Rect(pos_x, pos_y, self.assets['pic_size'], self.assets['pic_size'])

            if idx in self.flipped_cards or idx in self.matched_cards:
                if card == 'bomb':
                    self.screen.blit(self.assets['bomb_image'], rect)
                else:
                    image = pygame.image.load(f"Assets/object/{card}.png")
                    image = pygame.transform.scale(image, (self.assets['pic_size'], self.assets['pic_size']))
                    self.screen.blit(image, rect)
            else:
                pygame.draw.rect(self.screen, self.assets['GRAY'], rect)

    def check_match(self):
        if len(self.flipped_cards) == 2:
            idx1, idx2 = self.flipped_cards
            if self.cards[idx1] == self.cards[idx2]:
                if self.cards[idx1] == 'bomb':
                    # Shuffle unmatched cards
                    self.shuffle_cards()
                else:
                    self.matched_cards.update(self.flipped_cards)
            else:
                # Flip back if not a match
                pygame.time.wait(500)  # Brief delay for visualization
            self.flipped_cards = []

    def shuffle_cards(self):
        unmatched_indices = [
            i for i in range(len(self.cards)) if i not in self.matched_cards
        ]
        unmatched_cards = [self.cards[i] for i in unmatched_indices]
        random.shuffle(unmatched_cards)
        for i, idx in enumerate(unmatched_indices):
            self.cards[idx] = unmatched_cards[i]

    def is_game_over(self):
        elapsed_time = time.time() - self.start_time
        if len(self.matched_cards) == len(self.cards) - self.num_bombs:
            return "win"
        elif elapsed_time >= self.time_limit:
            return "lose"
        return None

    def handle_click(self, pos):
        for idx in range(len(self.cards)):
            x = idx % self.cols
            y = idx // self.cols
            pos_x = x * (self.assets['pic_size'] + self.assets['padding']) + self.assets['left_margin']
            pos_y = y * (self.assets['pic_size'] + self.assets['padding']) + self.assets['top_margin']
            rect = pygame.Rect(pos_x, pos_y, self.assets['pic_size'], self.assets['pic_size'])
            if rect.collidepoint(pos) and idx not in self.flipped_cards and idx not in self.matched_cards:
                self.flipped_cards.append(idx)
                break

    def game_loop(self):
        self.load_cards()
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.assets['bg_image'], (0, 0))
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.check_match()

            result = self.is_game_over()
            if result:
                return result

            pygame.display.update()
            clock.tick(30)
