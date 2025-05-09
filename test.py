from tkinter import *
import tkinter.font as tkFont
import pygame
from pygame.locals import *
import random
import sys
import math


class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x600")
        self.root.title("Math Exploration")

        # Define fonts
        self.font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        self.font_2 = tkFont.Font(family="Maximum Voltage", size=16, weight="bold")

        # Create frames
        self.frame_1 = Frame(self.root, bg="#e9c46a")
        self.frame_2 = Frame(self.root, bg="#f4a261")
        self.frame_1.place(relheight=0.5, relwidth=1, rely=0)
        self.frame_2.place(relheight=0.5, relwidth=1, rely=0.5)

        # Define a standard button width
        self.button_width = 12

        self.hardness_choice = "easy"

        self.setup_main_widgets()

        self.root.mainloop()

    def toggle_states(self, button, *texts):
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

    def hardness_choices(self, button):
        self.toggle_states(button, "Easy", "Medium", "Difficult")
        text = button.cget("text")
        if text == "Easy":
            self.hardness_choice = "easy"
        elif text == "Medium":
            self.hardness_choice = "medium"
        elif text == "Difficult":
            self.hardness_choice = "difficult"

    def clear_frame_2(self, next_menu="main"):
        """Clears frame_2 and loads either the main menu or the settings menu."""
        for widget in self.frame_2.winfo_children():
            widget.destroy()

        # Reset grid configurations before switching menus
        for i in range(4):  # Reset up to 4 rows
            self.frame_2.grid_rowconfigure(i, weight=0)
        for i in range(2):  # Reset up to 2 columns
            self.frame_2.grid_columnconfigure(i, weight=0)

        if next_menu == "settings":
            self.setup_setting_widgets()
        else:
            self.setup_main_widgets()

    def setup_main_widgets(self):
        """Creates main menu buttons inside frame_2 with proportional spacing."""

        # Configure grid for equal column and row distribution
        for i in range(2):
            self.frame_2.grid_rowconfigure(i, weight=1)  # Two rows
            self.frame_2.grid_columnconfigure(i, weight=1)  # Two columns

        Button(self.frame_2, text="Setting", font=self.font_1, width=self.button_width,
               command=lambda: self.clear_frame_2("settings")).grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10
        )
        Button(self.frame_2, text="Records", font=self.font_1, width=self.button_width).grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10
        )
        Button(self.frame_2, text="Quit", font=self.font_1, width=self.button_width, command=quit).grid(
            row=0, column=1, sticky="nsew", padx=10, pady=10
        )
        Button(self.frame_2, text="Start", font=self.font_1, width=self.button_width, command=self.start_game).grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10
        )

    def start_game(self):
        self.root.destroy()
        Game()

    def setup_setting_widgets(self):
        """Creates the setting menu in a 3:7 column ratio with 4 evenly spaced rows."""

        # Configure grid for 3:7 column ratio
        self.frame_2.grid_columnconfigure(0, weight=3)  # First column 30% width
        self.frame_2.grid_columnconfigure(1, weight=7)  # Second column 70% width

        # Configure 4 rows with equal height
        for i in range(4):
            self.frame_2.grid_rowconfigure(i, weight=1)

        Label(self.frame_2, text="Hardness", font=self.font_2, bg="#f4a261", anchor="w").grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10
        )

        # Set a fixed width for the hardness button
        hardness = Button(self.frame_2, text="Easy", font=self.font_2, width=10,
                          command=lambda: self.hardness_choices(hardness))
        hardness.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        Label(self.frame_2, text="Sound", font=self.font_2, bg="#f4a261", anchor="w").grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10
        )

        sound_switch = Button(self.frame_2, text="On", font=self.font_2, width=10,
                              command=lambda: self.toggle_states(sound_switch, "On", "Off"))
        sound_switch.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        Label(self.frame_2, text="Volume", font=self.font_2, bg="#f4a261", anchor="w").grid(
            row=2, column=0, sticky="nsew", padx=10, pady=10
        )
        Button(self.frame_2, text="Adjust", font=self.font_2, width=10).grid(
            row=2, column=1, sticky="nsew", padx=10, pady=10
        )

        Label(self.frame_2, text="Back", font=self.font_2, bg="#f4a261", anchor="w").grid(
            row=3, column=0, sticky="nsew", padx=10, pady=10
        )
        Button(self.frame_2, text="Return", font=self.font_2, width=10, command=self.clear_frame_2).grid(
            row=3, column=1, sticky="nsew", padx=10, pady=10
        )


class MathQizz:
    def __init__(self):
        self.num = random.randint(10, 500)  # Random number for the question
        self.correct_answer = math.sqrt(self.num)  # Compute the correct square root
        self.correct_answer = round(self.correct_answer, 2)


    def simple_questions(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(['+', '-', '*', '/'])

        if operation == '/':  # Ensure division results in whole numbers
            num1 = num1 * num2

        question = f"{num1} {operation} {num2}"
        answer = eval(question)
        return question, answer


    def medium_questions(self):

        question = f'''What is the approximate square root of {self.num}?'''

        # print("Welcome to 'Closest to the Answer'! Try to estimate the square root.")
        #
        # print(f"What is the approximate square root of {num}?")
        # user_guess = float(input("Your guess: "))
        #
        # error = abs(user_guess - correct_answer)
        # print(f"Actual answer: {correct_answer}")
        # print(f"Your error: {round(error, 2)}\n")


class Game:
    def __init__(self):
        # Pygame initialise
        pygame.init()
        self.math_window = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Math Questions")

        self.font = pygame.font.Font(None, 50)
        self.input_box = pygame.Rect(400, 300, 140, 50)

        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

        self.active = False
        self.text = ''
        self.score = 0

        self.math_quiz = MathQizz()
        self.question, self.correct_answer = self.math_quiz.simple_questions()

        self.result_text = ""

        while True:
            self.math_window.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Interface()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive

                if event.type == KEYDOWN:
                    if self.active:
                        if event.key == K_RETURN:
                            try:
                                if float(self.text) == self.correct_answer:
                                    self.result_text = "Correct!"
                                    self.score += 1
                                else:
                                    self.result_text = f"Wrong! Answer: {self.correct_answer}"
                                self.text = ''
                                self.question, self.correct_answer = self.math_quiz.simple_questions()
                            except ValueError:
                                self.result_text = "Enter a valid number!"
                        elif event.key == K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

            self.render_text(self.math_window, f"Solve: {self.question} = ?", (350, 200), self.font)
            self.render_text(self.math_window, f"Score: {self.score}", (50, 50), self.font)
            self.render_text(self.math_window, self.result_text, (350, 400), self.font, (255, 0, 0))

            pygame.draw.rect(self.math_window, self.color, self.input_box, 2)
            txt_surface = self.font.render(self.text, True, (0, 0, 0))
            self.math_window.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

            pygame.display.flip()

    def render_text(self, surface, text, pos, font, color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)


class TkinterMath:
    def __init__(self):
        self.math_questions = Toplevel(bg="#f4a261")


if __name__ == "__main__":
    Interface()
