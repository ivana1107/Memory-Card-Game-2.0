import pygame
from effects import Button

def EndScreen(screen, result, selected_level):
    pygame.init()
    pygame.mixer.init()

    # Load assets
    if result == "win":
        background = pygame.image.load("Assets/bg/win_screen.png")
        sound = pygame.mixer.Sound("Assets/win.wav")
        button_color = (66, 94, 150) 
    elif result == "lose":
        background = pygame.image.load("Assets/bg/lose_screen.png")
        sound = pygame.mixer.Sound("Assets/lose.wav")
        button_color = "white"
    else:
        raise ValueError("Invalid result: should be 'win' or 'lose'")

    # Play sound effect
    sound.play ()

    # Scale background to fit screen
    background = pygame.transform.scale(background, screen.get_size())

    # Buttons
    def get_font(size):
        return pygame.font.Font("Assets/Pixelicious.ttf", size)

    again_button = Button(image=None, pos=(405, 470), text_input="play again", font=get_font(45), base_color=button_color, hovering_color="yellow")
    back_button = Button(image=None, pos=(440, 550), text_input="back to menu", font=get_font(45), base_color=button_color, hovering_color="red")

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if again_button.checkForInput(mouse_pos):
                    return "play_again"
                if back_button.checkForInput(mouse_pos):
                    return "menu"

        # Draw background
        screen.blit(background, (0, 0))

        # Draw buttons and handle hover effect
        again_button.changeColor(mouse_pos)
        back_button.changeColor(mouse_pos)
        again_button.update(screen)
        back_button.update(screen)

        # Update display
        pygame.display.flip()