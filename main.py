import pygame
from start_screen import MemoryCardGame  # Import the game class from start_screen.py
from start_screen import main_menu  # Import main_menu from start_screen.py if needed

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load('Assets/star.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop

def main():
    """Main entry point for the game."""
    pygame.init()  # Initialize Pygame

    # Set up screen dimensions
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 760
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Memory Card Game")

    # Create an instance of MemoryCardGame
    game = MemoryCardGame(game_width=SCREEN_WIDTH, game_height=SCREEN_HEIGHT)
    
    # Call the main menu function to select difficulty
    selected_level = main_menu(game.screen)
    
    if not selected_level:
        print("No difficulty selected, exiting.")
        pygame.quit()
        return

    print(f"Starting game at {selected_level} difficulty.")
    
    # Run the game with the selected difficulty level
    game.run(selected_level)

    pygame.quit()

if __name__ == "__main__":
    main()

