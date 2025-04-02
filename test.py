from tkinter import *
import tkinter.font as tkFont
import pygame
from pygame.locals import *
import random
import sys
import math


def toggle_states(button, *texts):
    """Cycles through given states for any button."""
    levels = list(texts)  # Convert to list for indexing
    current_text = button.cget("text")

    if current_text in levels:
        # Find the next level in the cycle
        next_index = (levels.index(current_text) + 1) % len(levels)
    else:
        # Default to the first state if current_text is not found (failsafe)
        next_index = 0

    button.config(text=levels[next_index])


def clear_frame_2(next_menu="main"):
    """Clears frame_2 and loads either the main menu or the settings menu."""
    for widget in frame_2.winfo_children():
        widget.destroy()

    # Reset grid configurations before switching menus
    for i in range(4):  # Reset up to 4 rows
        frame_2.grid_rowconfigure(i, weight=0)
    for i in range(2):  # Reset up to 2 columns
        frame_2.grid_columnconfigure(i, weight=0)

    if next_menu == "settings":
        setup_setting_widgets()
    else:
        setup_main_widgets()


def hardness_choices(button):
    global hardness_choice
    toggle_states(button, "Easy", "Medium", "Difficult")
    if button.cget("text") == "Easy": hardness_choice = "easy"
    elif button.cget("text") == "Medium": hardness_choice = "medium"
    else: pass
    return hardness_choice


def setup_main_widgets():
    """Creates main menu buttons inside frame_2 with proportional spacing."""

    # Configure grid for equal column and row distribution
    for i in range(2):
        frame_2.grid_rowconfigure(i, weight=1)  # Two rows
        frame_2.grid_columnconfigure(i, weight=1)  # Two columns

    # Define a standard button width
    button_width = 12

    Button(frame_2, text="Setting", font=font_1, width=button_width, command=lambda: clear_frame_2("settings")).grid(
        row=0, column=0, sticky="nsew", padx=10, pady=10
    )
    Button(frame_2, text="Records", font=font_1, width=button_width).grid(
        row=1, column=0, sticky="nsew", padx=10, pady=10
    )
    Button(frame_2, text="Quit", font=font_1, width=button_width, command=quit).grid(
        row=0, column=1, sticky="nsew", padx=10, pady=10
    )
    Button(frame_2, text="Start", font=font_1, width=button_width, command=game_main).grid(
        row=1, column=1, sticky="nsew", padx=10, pady=10
    )


def setup_setting_widgets():
    """Creates the setting menu in a 3:7 column ratio with 4 evenly spaced rows."""

    # Configure grid for 3:7 column ratio
    frame_2.grid_columnconfigure(0, weight=3)  # First column 30% width
    frame_2.grid_columnconfigure(1, weight=7)  # Second column 70% width

    # Configure 4 rows with equal height
    for i in range(4):
        frame_2.grid_rowconfigure(i, weight=1)

    Label(frame_2, text="Hardness", font=font_2, bg="#f4a261", anchor="w").grid(
        row=0, column=0, sticky="nsew", padx=10, pady=10
    )

    # Set a fixed width for the hardness button
    hardness = Button(frame_2, text="Easy", font=font_2, width=10,
                      command=lambda: hardness_choices(hardness))
    hardness.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    Label(frame_2, text="Sound", font=font_2, bg="#f4a261", anchor="w").grid(
        row=1, column=0, sticky="nsew", padx=10, pady=10
    )

    sound_switch = Button(frame_2, text="On", font=font_2, width=10,
                          command=lambda: toggle_states(sound_switch, "On", "Off"))
    sound_switch.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    Label(frame_2, text="Volume", font=font_2, bg="#f4a261", anchor="w").grid(
        row=2, column=0, sticky="nsew", padx=10, pady=10
    )
    Button(frame_2, text="Adjust", font=font_2, width=10).grid(
        row=2, column=1, sticky="nsew", padx=10, pady=10
    )

    Label(frame_2, text="Back", font=font_2, bg="#f4a261", anchor="w").grid(
        row=3, column=0, sticky="nsew", padx=10, pady=10
    )
    Button(frame_2, text="Return", font=font_2, width=10, command=clear_frame_2).grid(
        row=3, column=1, sticky="nsew", padx=10, pady=10
    )

def simple_questions():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*', '/'])

    if operation == '/':  # Ensure division results in whole numbers
        num1 = num1 * num2

    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    return question, answer


def medium_questions():
    num = random.randint(10, 500)
    correct_answer = round(math.sqrt(num), 2)
    return f"What is the approximate square root of {num}?", correct_answer

def render_text(surface, text, pos, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def game_main():
    root.destroy()
    pygame.init()
    math_window = pygame.display.set_mode((960, 540))
    pygame.display.set_caption("Math Questions")
    font = pygame.font.Font(None, 50)
    input_box = pygame.Rect(400, 300, 140, 50)
    color_inactive, color_active = pygame.Color('lightskyblue3'), pygame.Color('dodgerblue2')
    color, active, text, score = color_inactive, False, '', 0

    def get_question():
        if hardness_choice == "easy": return simple_questions()
        elif hardness_choice == "medium": return medium_questions()
        return "TBD", 0  # Placeholder for "Difficult"
    question, correct_answer = get_question()
    result_text = ""

    while True:
        math_window.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                main()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == KEYDOWN and active:
                if event.key == K_RETURN:
                    try:
                        if float(text) == correct_answer:
                            result_text, score = "Correct!", score + 1
                        else:
                            result_text = f"Wrong! Answer: {correct_answer}"
                        text, question, correct_answer = '', *get_question()
                    except ValueError:
                        result_text = "Enter a valid number!"
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        math_window.blit(font.render(f"Solve: {question} = ?", True, (0, 0, 0)), (350, 200))
        math_window.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (50, 50))
        math_window.blit(font.render(result_text, True, (255, 0, 0)), (350, 400))
        pygame.draw.rect(math_window, color, input_box, 2)
        math_window.blit(font.render(text, True, (0, 0, 0)), (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()


def main():
    global frame_1, frame_2, font_1, font_2, root
    root = Tk()
    root.geometry("400x600")
    root.title("Math Exploration")

    # Define fonts
    font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
    font_2 = tkFont.Font(family="Maximum Voltage", size=16, weight="bold")

    # Create frames
    frame_1 = Frame(root, bg="#e9c46a")
    frame_2 = Frame(root, bg="#f4a261")
    frame_1.place(relheight=0.5, relwidth=1, rely=0)
    frame_2.place(relheight=0.5, relwidth=1, rely=0.5)

    setup_main_widgets()

    root.mainloop()

hardness_choice = "easy"

if __name__ == "__main__":
    main()
