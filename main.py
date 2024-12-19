import pygame
from start_screen import main_menu
from start_screen import MemoryCardGame
from game_logic import GameLogic
from end_screen import EndScreen  # Import the EndScreen function

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
# pygame.mixer.music.load('Assets/star.mp3')
# pygame.mixer.music.play(-1)  # Play music in a loop

def main():
    """Main entry point for the game."""

    # Set up screen dimensions
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 760
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flip and Find")

    memory_game = MemoryCardGame()
    memory_game.load_assets()

    # Initialize assets dictionary
    assets = {
        'memory_pictures': memory_game.memory_pictures,
        'pic_size': memory_game.pic_size,
        'padding': memory_game.padding,
        'left_margin': memory_game.left_margin,
        'top_margin': memory_game.top_margin,
        'bg_image': memory_game.bg_image,
        'bomb_image': memory_game.bomb_image,
        'GRAY': memory_game.GRAY,
        'game_width': SCREEN_WIDTH,
        'game_height': SCREEN_HEIGHT
    }

    # Create the Game instance outside the loop
    game = GameLogic(screen, None, assets)  # Initialize with None for difficulty

    selected_level = None

    while True:  # Main game loop
        # Get difficulty level from menu only if it's not set
        if selected_level is None:
            selected_level = main_menu(screen)
            if not selected_level:
                pygame.quit()
                return

        # Reinitialize the game logic for a new game
        game.difficulty = selected_level
        game.reset_game()

        result = game.game_loop()

        # Handle game result and show end screen
        if result:
            action = EndScreen(screen, result, selected_level)
            if action == "play_again":
                # Keep the current difficulty level
                game.reset_game()
                continue  # Start a new game with the same difficulty
            elif action == "menu":
                selected_level = None  # Reset difficulty to trigger main menu on next iteration
            else:
                break

    pygame.quit()

if __name__ == "__main__":
    main()