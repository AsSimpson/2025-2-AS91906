from tkinter import *
import tkinter.font as tkFont
import random


class FontManager:
    def __init__(self):
        self.font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        self.font_1_medium = tkFont.Font(family="Agency FB", size=30, weight="bold")
        self.font_2 = tkFont.Font(family="Georgia", size=16, weight="bold")
        self.font_2_medium = tkFont.Font(family="Georgia", size=30, weight="bold")


class MathQuestion:
    def __init__(self):
        self.a = random.randint(10, 20)
        self.b = random.randint(10, 20)
        self.sign = random.choice(['+', '-', 'x', '/'])

        if self.sign == '/':
            self.a *= self.b

        self.answer = self.compute_answer()

    def compute_answer(self):
        return {
            '+': self.a + self.b,
            '-': self.a - self.b,
            'x': self.a * self.b,
            '/': self.a / self.b
        }[self.sign]

    def get_question_text(self):
        return f"Find the value of {self.a} {self.sign} {self.b}."


class MathQuizlet:
    def __init__(self, parent, fonts):
        self.question = MathQuestion()
        self.fonts = fonts
        self.quiz_window = Toplevel(parent)
        self.quiz_window.geometry("500x400")
        self.quiz_window.configure(bg="lightblue")

        self.user_input = StringVar()
        self.create_widgets()

    def create_widgets(self):
        Label(self.quiz_window, text=self.question.get_question_text(),
              font=self.fonts.font_2, bg='lightblue').grid(
            column=0, row=0, padx=20, pady=20, columnspan=2, sticky='nsew')

        Entry(self.quiz_window, textvariable=self.user_input).grid(
            column=0, row=1, padx=20, pady=20, sticky='nsew')

        Button(self.quiz_window, text='Submit', command=self.check_answer).grid(
            column=1, row=1, padx=20, pady=20, sticky='nsew')

    def check_answer(self):
        try:
            if float(self.user_input.get()) == self.question.answer:
                result = "Correct"
                color = "green"
            else:
                result = "Wrong"
                color = "red"
        except ValueError:
            result = "Invalid input"
            color = "orange"

        Label(self.quiz_window, text=result, font=self.fonts.font_2, fg=color, bg='lightblue').grid(
            column=0, row=2, columnspan=2, pady=10)


class Menu:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x500")
        self.root.title("Math Quizlet")
        self.root.configure(bg="#9A4C95")

        self.fonts = FontManager()

        self.create_main_menu()
        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        Button(self.root, text="Start", font=self.fonts.font_1, bg="#F08CAE",
               command=self.start_quiz).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Records", font=self.fonts.font_1, bg="#F08CAE").grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Settings", font=self.fonts.font_1, bg="#F08CAE",
               command=self.create_settings_menu).grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Quit", font=self.fonts.font_1, bg="#F08CAE", command=quit).grid(
            row=3, column=0, sticky="nsew", padx=10, pady=10)

    def create_settings_menu(self):
        self.clear_window()
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        Button(self.root, text="Hardness", font=self.fonts.font_1, bg="#F08CAE").grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Sound", font=self.fonts.font_1, bg="#F08CAE").grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Background Color", font=self.fonts.font_1, bg="#F08CAE").grid(
            row=2, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Go Back", font=self.fonts.font_1, bg="#F08CAE",
               command=self.create_main_menu).grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    def start_quiz(self):
        MathQuizlet(self.root, self.fonts)


if __name__ == "__main__":
    Menu()
