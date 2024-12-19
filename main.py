import pygame
from start_screen import main_menu  # Import main_menu from start_screen.py if needed
from start_screen import MemoryCardGame
from game_logic import GameLogic

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

    # Call the main menu function to select difficulty
    selected_level = main_menu(screen)
    if not selected_level:
        pygame.quit()
        return
    
    # Initialize the Game object with selected difficulty and other assets
    assets = {
        'memory_pictures': memory_game.memory_pictures, 
        'pic_size': memory_game.pic_size,  # Size of cards
        'padding': memory_game.padding,  # Padding between cards
        'left_margin': memory_game.left_margin,
        'top_margin': memory_game.top_margin,
        'bg_image': memory_game.bg_image,
        'bomb_image' : memory_game.bomb_image,
        'GRAY' : memory_game.GRAY,
        'game_width': SCREEN_WIDTH,
        'game_height': SCREEN_HEIGHT
    }

    # Create the Game instance
    game = GameLogic(screen, selected_level, assets)
    result = game.game_loop()

    if result == "win":
        print("You won!")
    elif result == "lose":
        print("You lost!")

    pygame.quit()

if __name__ == "__main__":
    main()