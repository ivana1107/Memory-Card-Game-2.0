import pygame

def get_font(size):
    """Returns a Pygame font object."""
    return pygame.font.Font("Assets/Pixelicious.ttf", size)

class Button:
    def __init__(self, image, pos, text_input, font=None, font_path=None, font_size=30, base_color="white", hovering_color="yellow"):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("Assets/tap.wav")

        # Set up button appearance
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """Draw the button on the screen."""
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def changeColor(self, position):
        """Change the button text color based on hover state."""
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def play_click_sound(self):
        self.sound.play()

    def checkForInput(self, position):
        """Check if the button is clicked."""
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.play_click_sound()
            return True
        return False

