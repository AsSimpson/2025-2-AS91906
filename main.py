from tkinter import *
import tkinter.font as tkFont
import random


class Menu:
    def __init__(self):
        # Configure menu window
        self.root = Tk()
        self.root.geometry("400x500")
        self.root.title("Math quizlet")

        # Define fonts
        global font_1, font_1_medium, font_2, font_2_medium
        font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        font_1_medium = tkFont.Font(family="Agency FB", size=30, weight="bold")
        font_2 = tkFont.Font(family="Georgia", size=16, weight="bold")
        font_2_medium = tkFont.Font(family="Georgia", size=30, weight="bold")

        self.widget()

        self.root.mainloop()

    def widget(self):
        self.root.grid_columnconfigure(0, weight=1)
        # Configure 4 rows with equal height
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        Button(self.root, text = "Start", font = font_1, command=MathQuizlet).grid(
            column=0, row=0, sticky="nsew", padx=10, pady=10
        )
        Button(self.root, text = "Records", font = font_1).grid(
            column=0, row=1, sticky="nsew", padx=10, pady=10
        )
        Button(self.root, text = "Settings", font = font_1).grid(
            column=0, row=2, sticky="nsew", padx=10, pady=10
        )
        Button(self.root, text='Quit', font=font_1, command=quit).grid(
            column=0, row=3, sticky='nsew', padx=10, pady=10
        )



class MathQuizlet:
    def __init__(self):
        self.quiz_window = Toplevel(bg="lightblue")
        self.quiz_window.geometry("500x400")

        self.a = random.randint(10, 20)
        self.b = random.randint(10, 20)
        self.sign = random.choice(['+', '-', 'x', '/'])

        self.answer = None
        self.user_answer = None
        self.result = None

        if self.sign == '/': self.a = self.a * self.b

        self.question = f'''Find the value of {self.a} {self.sign} {self.b}.'''

        if self.sign == '+':
            self.answer = self.a + self.b
        elif self.sign == '-':
            self.answer = self.a - self.b
        elif self.sign == 'x':
            self.answer = self.a * self.b
        elif self.sign == '/':
            self.answer = self.a / self.b


        self.quiz_widgets()

    def quiz_widgets(self):
        Label(self.quiz_window, text=self.question, font=font_2, bg='lightblue').grid(
            column=0, row=0, padx=20, pady=20, sticky='nsew'
        )
        self.user_answer = Entry(self.quiz_window)
        self.user_answer.grid(
            column=0, row=1, padx=20, pady=20, sticky='nsew'
        )
        Button(self.quiz_window, text='Submit', command=self.check_answer).grid(
            column=1, row=1, padx=20, pady=20, sticky='nsew'
        )

    def check_answer(self):
        if self.user_answer == self.answer: self.result = "Correct"; result_colour='green'
        else: self.result = "Wrong"; result_colour = 'red'
        Label(self.quiz_window, text=self.result, font=font_2, fg=result_colour).grid(
            column=0, row=2, padx=20, pady=20, sticky='nsew'
        )


math_quiz = Menu

if __name__ == "__main__":
    math_quiz()

