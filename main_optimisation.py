from tkinter import *
import tkinter.font as tkFont
import random


def pin_window(parent, button):
    if str(button['bg']) != 'gray':
        parent.attributes('-topmost', True)
        button.configure(bg='gray', text="Unpin Window")
    elif str(button['bg']) == 'gray':
        parent.attributes('-topmost', False)
        button.configure(bg='SeaGreen3', text="Pin Window")


class Fonts:
    def __init__(self):
        self.font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        self.font_1_big = tkFont.Font(family="Agency FB", size=30, weight="bold")
        self.font_2 = tkFont.Font(family="Georgia", size=16, weight="bold")
        self.font_2_big = tkFont.Font(family="Georgia", size=30, weight="bold")


class MathQuestions:
    def __init__(self):
        self.a = random.randint(0,20)
        self.b = random.randint(0, 20)
        self.sign = random.choice(['+', '-', 'x', '/'])

        if self.sign == '/': self.a *= self.b

        self.answer = self.compute_answer()

    def compute_answer(self):
        if self.sign == '+': return self.a + self.b
        if self.sign == '-': return self.a - self.b
        if self.sign == 'x': return  self.a * self.b
        else: return self.a / self.b

    def __str__(self):
        return f'''Find out the answer of {self.a} {self.sign} {self.b}'''


class MathWindow:
    def __init__(self, parent, font):
        self.question = MathQuestions()
        self.font = font
        self.question_win = Toplevel(parent)
        self.question_win.geometry("500x400")
        self.question_win.configure(bg="#00C49A")

        self.question_win.bind('<Return>', lambda event: self.check())

        self.input = StringVar()
        self.widgets()

    def widgets(self):
        self.question_label = Label(self.question_win, text=str(self.question),
                                    font=self.font.font_2, bg='#00C49A')
        self.question_label.grid(column=0, row=0, padx=20, pady=20, columnspan=2, sticky='nsew')

        self.answer_entry = Entry(self.question_win, textvariable=self.input)
        self.answer_entry.grid(column=0, row=1, padx=20, pady=20, sticky='nsew')

        Button(self.question_win, text='Submit', command=self.check).grid(
            column=1, row=1, padx=20, pady=20, sticky='nsew')

        self.pin_win = Button(self.question_win, text='pin window', bg='SeaGreen3', command=lambda: pin_window(self.question_win, self.pin_win))
        self.pin_win.grid(column=2, row=1, padx=20, pady=20, sticky='nsew')

        self.result_label = Label(self.question_win, font=self.font.font_2, bg="#00C49A")
        self.result_label.grid(column=0, row=2, columnspan=2, pady=10)

    def check(self):
        try:
            if int(self.input.get()) == self.question.answer:
                  result = "Correct"; colour = 'green'
            else: result = "Wrong";   colour = 'red'
        except ValueError:
            result = "Invalid input"; colour = 'orange'

        Label(self.question_win, text = result, font=self.font.font_2, bg="#00C49A").grid(
            column=0, row=2, columnspan=2, pady=10
        )
        # Refresh question after a short delay
        self.question_win.after(400, self.refresh)  # delay for UX

    def refresh(self):
        self.question = MathQuestions()
        self.input.set("")  # clear entry field
        self.question_label.config(text=str(self.question))
        self.answer_entry.focus()
        self.result_label.config(text="")  # Clear previous result
        Label(self.question_win, text='                                      ', font=self.font.font_2,
              bg="#00C49A").grid(column=0, row=2, columnspan=2, pady=10)



class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x500")
        self.root.title("Math Quizlet")
        self.root.configure(bg="lightgreen")

        self.fonts = Fonts()

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

        Button(self.root, text="Start", font=self.fonts.font_1, bg="SeaGreen3",
               command=self.start_quiz).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Records", font=self.fonts.font_1, bg="SeaGreen3").grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Settings", font=self.fonts.font_1, bg="SeaGreen3",
               command=self.create_settings_menu).grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Quit", font=self.fonts.font_1, bg="SeaGreen3", command=quit).grid(
            row=3, column=0, sticky="nsew", padx=10, pady=10)

    def create_settings_menu(self):
        self.clear_window()
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        Button(self.root, text="Hardness", font=self.fonts.font_1, bg="SeaGreen3").grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Sound", font=self.fonts.font_1, bg="SeaGreen3").grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Background Color", font=self.fonts.font_1, bg="SeaGreen3").grid(
            row=2, column=0, sticky="nsew", padx=10, pady=10)

        Button(self.root, text="Go Back", font=self.fonts.font_1, bg="SeaGreen3",
               command=self.create_main_menu).grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    def start_quiz(self):
        MathWindow(self.root, self.fonts)

if __name__ == "__main__":
    MainWindow()