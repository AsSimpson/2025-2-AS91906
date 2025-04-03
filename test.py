import pygame
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


pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Text Input")

# Font & Colors
font = pygame.font.Font(None, 40)
color_active = (0, 200, 0)  # Green when active
color_inactive = (200, 200, 200)  # Gray when inactive

# Create input box instance
input_box = TextInputBox(250, 250, 300, 50, font, color_active, color_inactive)

running = True
while running:
    screen.fill((30, 30, 30))  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)  # Handle typing

    input_box.draw(screen)  # Draw input box
    pygame.display.update()

pygame.quit()
