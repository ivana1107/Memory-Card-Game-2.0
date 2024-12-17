import pygame
import random
import time
from timer import timer

class GameLogic:
    def __init__(self, screen, difficulty, assets):
        self.screen = screen
        self.difficulty = difficulty
        self.assets = assets
        self.rows, self.cols, self.num_bombs = self.get_level_config()
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = set()
        self.bomb_indices = []
        self.bomb_shuffled = False
        self.game_timer = timer(screen, pygame.font.Font('Assets/Pixelicious.ttf', 45), difficulty)

    def get_level_config(self):
        if self.difficulty == "easy":
            return 3, 3, 1
        elif self.difficulty == "medium":
            return 4, 4, 2
        elif self.difficulty == "hard":
            return 5, 5, 3

    def load_cards(self):
        # Select images for pairs and bomb
        num_pairs = (self.rows * self.cols - self.num_bombs) // 2
        images = random.sample(self.assets['memory_pictures'], num_pairs)
        images *= 2  # Duplicate images to form pairs
        images += ['bomb'] * self.num_bombs
        random.shuffle(images)
        self.cards = images
        self.bomb_indices = [i for i, card in enumerate(self.cards) if card == 'bomb']

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
            card1, card2 = self.cards[idx1], self.cards[idx2]
            if card1 == 'bomb' or card2 == 'bomb':
                # Bomb triggered: Shuffle unmatched cards and keep bomb open
                if not self.bomb_shuffled:
                    self.shuffle_unmatched_cards()
                    self.bomb_shuffled = True
                self.matched_cards.update([idx1, idx2])  # Bomb stays open
            elif card1 == card2:
                # Match found: Keep cards open
                self.matched_cards.update(self.flipped_cards)
            else:
                # No match: Brief delay and flip back
                pygame.display.update()
                pygame.time.wait(700)

            self.flipped_cards = []

    def shuffle_unmatched_cards(self):
        # Shuffle all unmatched cards except for already matched cards and flipped bombs
        unmatched_indices = [
            i for i in range(len(self.cards)) if i not in self.matched_cards and self.cards[i] != 'bomb'
        ]
        unmatched_cards = [self.cards[i] for i in unmatched_indices]
        random.shuffle(unmatched_cards)

        # Reassign shuffled cards to their indices
        for i, idx in enumerate(unmatched_indices):
            self.cards[idx] = unmatched_cards[i]


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

            if len(self.matched_cards) == len(self.cards) - self.num_bombs:
                return "win"

            pygame.display.update()
            clock.tick(30)
