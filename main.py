import pygame
from start_screen import main_menu # Import main_menu from start_screen.py if needed
from start_screen import MemoryCardGame
from start_screen import Level

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
    
    # Call the main menu function to select difficulty
    selected_level = main_menu(screen)
    
    if not selected_level:
        print("No difficulty selected, exiting.")
        pygame.quit()
        return

    print(f"Starting game at {selected_level} difficulty.")
    
     # Initialize the Game object with selected difficulty and other assets
    assets = {
        'memory_pictures': [],  # List your memory pictures here
        'pic_size': 128,  # Size of cards
        'padding': 10,  # Padding between cards
        'left_margin': 75,
        'top_margin': 70,
        'bg_image': pygame.image.load('Assets/bg/game_layout.png')
    }

    # Create the Game instance
    game_instance = MemoryCardGame(screen, selected_level, assets)

    # Run the game with the selected difficulty level
    game_instance.game_loop() 

    pygame.quit()

if __name__ == "__main__":
    main()

