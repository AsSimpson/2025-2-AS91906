import pygame
import random
import math

class TextInputBox:
    def __init__(self, x, y, w, h, font, color_active, color_inactive):
        self.rect = pygame.Rect(x, y, w, h)  # Input box dimensions
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = color_inactive  # Default state
        self.text = ""  # Stores user input
        self.font = font
        self.active = False  # Whether the box is active

    def handle_event(self, event):
        """Handles user input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If user clicks inside the box, activate input
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:  # Press Enter to submit
                    print(f"User entered: {self.text}")  # You can use the text here
                    self.text = ""  # Clear text after Enter
                elif event.key == pygame.K_BACKSPACE:  # Backspace removes last char
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # Add typed character

    def draw(self, screen):
        """Renders the input box and text."""
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw box border
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Render text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Blit text


def medium_questions():
    num = random.randint(10, 500)  # Random number for the question
    correct_answer = math.sqrt(num)  # Compute the correct square root
    correct_answer = round(correct_answer, 2)

    question = f'''What is the approximate square root of {num}?'''

    # print("Welcome to 'Closest to the Answer'! Try to estimate the square root.")
    #
    # print(f"What is the approximate square root of {num}?")
    # user_guess = float(input("Your guess: "))
    #
    # error = abs(user_guess - correct_answer)
    # print(f"Actual answer: {correct_answer}")
    # print(f"Your error: {round(error, 2)}\n")
    return question, correct_answer


import pygame


def render_text_wrapped(text, font, color, max_width, start_pos, surface):
    """
    Renders and wraps text to fit within max_width.

    Parameters:
        text (str): The text to render
        font (pygame.font.Font): Font object
        color (tuple): RGB color
        max_width (int): Maximum width for wrapping
        start_pos (tuple): (x, y) position of top-left text start
        surface (pygame.Surface): The screen or surface to draw on
    """
    words = text.split(" ")  # Split text into words
    lines = []  # List to store wrapped lines
    line = ""  # Current line being built

    for word in words:
        # Render line temporarily to check width
        test_line = line + word + " "
        test_surface = font.render(test_line, True, color)

        if test_surface.get_width() > max_width:  # If too wide, start a new line
            lines.append(line)  # Store the finished line
            line = word + " "  # Start a new line with the current word
        else:
            line = test_line  # Add word to the current line

    lines.append(line)  # Append the last line

    # Render and display lines
    x, y = start_pos
    line_height = font.get_height()  # Get font height for spacing

    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y))
        y += line_height  # Move to the next line


pygame.init()

width, height = 960, 540
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Math Display")

# Import font assets
font_1 = pygame.font.Font("assets/fonts/Agency FB.TTF", 40)
font_2 = pygame.font.Font("assets/fonts/Maximum Voltage.otf", 36)

# Import background assets
background_1 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_1.png').convert_alpha()
background_2 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_2.png').convert_alpha()
background_3 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_3.png').convert_alpha()

background_1 = pygame.transform.rotozoom(background_1, 0, 3)
background_2 = pygame.transform.rotozoom(background_2, 0, 3)
background_3 = pygame.transform.rotozoom(background_3, 0, 3)


# Import character assets
blue_stand_surf = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/character/char_blue_standby_1.png').convert_alpha()
blue_stand_rect = blue_stand_surf.get_rect()

# Render texts
questions_surf = font_1.render("What is the product of 1 and 4?", True, "black")
questions_rect = questions_surf.get_rect(center = (width//2, height//2 - 150))

question, correct_answer = medium_questions()

game_state = True

while game_state:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game_screen.blit(background_1, (0, 0))
    game_screen.blit(background_2, (0, 0))
    game_screen.blit(background_3,  (0,0))

    render_text_wrapped(question, font_1, (0,0,0), width, (50, 50), game_screen)

    pygame.display.update()
