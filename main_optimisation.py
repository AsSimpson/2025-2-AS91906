from tkinter import *
from tkinter.ttk import Combobox
import tkinter.font as tkFont
import random
import os


def pin_window(parent, button):
    if str(button['bg']) != 'gray':
        parent.attributes('-topmost', True)
        button.configure(bg='gray', text="Unpin Window")
    elif str(button['bg']) == 'gray':
        parent.attributes('-topmost', False)
        button.configure(bg='SeaGreen3', text="Pin Window")


class ToggleButton:
    def __init__(self, button, texts, colors=None, on_change=None, start_index=0):
        self.button = button
        self.texts = list(texts)
        self.colors = list(colors) if colors else [button.cget("bg"), 'gray']
        self.index = start_index
        self.on_change = on_change
        self.apply_state()
        self.button.config(command=self.toggle)

    def apply_state(self):
        text = self.texts[self.index]
        color = self.colors[self.index % len(self.colors)]
        self.button.config(text=text, bg=color)
        if self.on_change:
            self.on_change(text)

    def toggle(self):
        self.index = (self.index + 1) % len(self.texts)
        self.apply_state()


class Fonts:
    def __init__(self):
        self.font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        self.font_1_big = tkFont.Font(family="Agency FB", size=30, weight="bold")
        self.font_2 = tkFont.Font(family="Georgia", size=16, weight="bold")
        self.font_2_big = tkFont.Font(family="Georgia", size=30, weight="bold")

        self.fontNum1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
        self.fontNum2 = tkFont.Font(family="Agency FB", size=30, weight="bold")
        self.fontNum3 = tkFont.Font(family="Arial", size=11, weight="bold")
        self.fontNum4 = tkFont.Font(family="Cooper Black", size=18, weight='normal')



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

        self.time_left = 5  # seconds
        self.timer_label = Label(self.question_win, text=f"Time: {self.time_left}", font=self.font.font_2, bg="#00C49A")
        self.timer_label.grid(column=2, row=0, padx=10, pady=10)
        self.timer()

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

    def check(self, disable_check=False):
        try:
            user_val = float(self.input.get())
            if self.input == self.question.answer:
                result = "Correct"
                colour = 'green'
            else:
                result = "Wrong"
                colour = 'red'
        except ValueError:
            result = "Invalid input"
            colour = 'orange'

        self.result_label.config(text=result, fg=colour)

        # Stop further input
        if disable_check:
            self.answer_entry.config(state="disabled")

        self.question_win.after(1000, self.refresh)

    def refresh(self):
        self.question = MathQuestions()
        self.input.set("")  # clear entry field
        self.question_label.config(text=str(self.question))
        self.answer_entry.focus()
        self.result_label.config(text="")  # Clear previous result
        Label(self.question_win, text='                                      ', font=self.font.font_2,
              bg="#00C49A").grid(column=0, row=2, columnspan=2, pady=10)

        self.time_left = 5
        self.timer()

    def timer(self):
        self.timer_label.configure(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.question_win.after(1000, self.timer)
        else:
            self.input.set("Time's up!")
            self.check(disable_check=True)


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("750x650")
        self.root.title("Math Quizlet")
        self.root.configure(bg="lightgreen")

        self.settings = {
            'sound': 'ON',
            'difficulty': 'Normal',
            'background': 'lightgreen'
        }

        self.fonts = Fonts()
        self.sound_switch_toggle = None

        self.create_main_menu()
        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        # Main columns
        main_f = Frame(self.root)
        main_f.place(anchor=NW, relx=0, rely=0, relheight=1, relwidth=1)

        # Create two frames to sort out all the widgets: Top one:
        top = (Frame(main_f, bg='yellow'))
        top.place(anchor=NW, rely=0.25, relheight=0.35, relwidth=1)
        # Create all the labels, buttons, and entry boxes. Put them in the correct grid location
        Label(top, text="Name", bg="orange", font=self.fonts.fontNum1).grid(
            column=0, row=0, padx=20, pady=25, sticky=W)
        Label(top, text="Items Hired", bg="orange", font=self.fonts.fontNum1).grid(
            column=0, row=1, padx=20, pady=25, sticky=W)
        Label(top, text="Receipt Number", bg="orange", font=self.fonts.fontNum1).grid(
            column=2, row=0, padx=20, pady=25, sticky=W)
        Button(top, text="Random Number", bg="tomato", bd=5, font=self.fonts.fontNum3, height=1).grid(
            column=5, row=0, pady=30, sticky='NW')
        Label(top, text="Hired Amount", bg="orange", font=self.fonts.fontNum1).grid(
            column=2, row=1, padx=20, pady=25, sticky=W)

        # Get purchase information from user input
        entry_name = Entry(top, width=23)
        entry_name.grid(column=1, row=0, sticky=W)
        entry_receipt_number = Entry(top, width=23)
        entry_receipt_number.grid(column=3, row=0, sticky=W)
        entry_items_number = Entry(top, width=23)
        entry_items_number.grid(column=3, row=1, sticky=W)

        # create combobox
        purchase_list = ['Tables', 'Balloons', 'Party Hats', 'Snacks', 'Drinks', 'Serving Bowls']
        entry_item = Combobox(top, values=purchase_list, state='readonly')
        entry_item.grid(column=1, row=1, sticky=W)
        entry_item.set("Please choose an item name. ")

        # Middle Frame:
        middle = Frame(main_f, bg='orange')
        middle.place(relheight=0.4, relwidth=1, rely=0.6)
        button_pin = Button(middle, text="Pin Window", font=self.fonts.fontNum1, width=20, height=1, bg='SeaGreen3', bd=10,
                            relief='raised', state='normal', compound=LEFT)
        button_pin.grid(column=0, row=0, padx=10, sticky='NW')
        Button(middle, text="Submit", font=self.fonts.fontNum1, width=20, height=1, bg='OliveDrab1', bd=10, relief='raised'
               , compound=LEFT).grid(column=1, row=0, padx=20, sticky='NW')
        Button(middle, text="START", fg='red', font=self.fonts.fontNum1, width=20, height=1, bg='yellow2', bd=10,
               relief='raised', command=self.start_quiz).grid(column=2, row=0, padx=10, sticky='NW')
        Button(middle, text="Quit", font=self.fonts.fontNum1, height=1, width=20, bg='red', bd=10, command=quit).grid(
            column=0, row=1, padx=10, pady=12, sticky=W)

        setting = Button(middle, text="Setting", font=self.fonts.fontNum1, height=1, width=20, bg='PaleGreen2', bd=10,
                         relief='raised', command=self.create_settings_menu)
        setting.grid(column=2, row=1, padx=10, pady=12)

        # self.clear_window()
        # self.root.grid_columnconfigure(0, weight=1)
        # for i in range(4):
        #     self.root.grid_rowconfigure(i, weight=1)
        # 
        # Button(self.root, text="Start", font=self.fonts.font_1, bg="SeaGreen3",
        #        command=self.start_quiz).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # 
        # Button(self.root, text="Records", font=self.fonts.font_1, bg="SeaGreen3").grid(
        #     row=1, column=0, sticky="nsew", padx=10, pady=10)
        # 
        # Button(self.root, text="Settings", font=self.fonts.font_1, bg="SeaGreen3",
        #        command=self.create_settings_menu).grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        # 
        # Button(self.root, text="Quit", font=self.fonts.font_1, bg="SeaGreen3", command=quit).grid(
        #     row=3, column=0, sticky="nsew", padx=10, pady=10)


    def save_receipt_to_file(self, button):
        # if not os.path.exists('savedata'):
        #     os.makedirs('savedata')
        # with open(f'savedata/{button}.txt', 'w') as file:
        #     file.write(f"sound: {self.sound_switch_toggle.current_text}\n")
        #     file.write(f"difficulty: {entry_ItemsPurchased.get()}\n")
        #     file.write(f"background: {entry_ItemsNumber.get()}\n")
        pass


    def create_settings_menu(self):
        self.clear_window()
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=7)

        Label(self.root, text="Difficulty", font=self.fonts.font_1, bg="lightgreen", width=30, height=1).grid(
            row=0, column=0, sticky="nw", padx=10, pady=10
        )
        Label(self.root, text="Sound", font=self.fonts.font_1, bg="lightgreen", width=30, height=1).grid(
            row=1, column=0, sticky="nw", padx=10, pady=10
        )
        Label(self.root, text="Background Color", font=self.fonts.font_1, bg="lightgreen", width=30, height=1).grid(
            row=2, column=0, sticky="nw", padx=10, pady=10
        )
        Label(self.root, text="Go Back", font=self.fonts.font_1, bg="lightgreen", width=30, height=1).grid(
            row=3, column=0, sticky="nw", padx=10, pady=10)

        Button(self.root, text="Difficulty", font=self.fonts.font_1, bg="SeaGreen3", width=70, height=1).grid(
            row=0, column=1, sticky="nw", padx=10, pady=10)

        sound_switch = Button(self.root, text="On", font=self.fonts.font_1, bg="SeaGreen3", width=70, height=1)
        sound_switch.grid(row=1, column=1, sticky="nw", padx=10, pady=10)

        # Restore previous state when recreating the button
        initial_state = self.settings['sound']
        start_index = 0 if initial_state == 'ON' else 1
        ToggleButton(sound_switch, ['ON', 'OFF'], on_change=lambda val: self.settings.update({'sound': val}), start_index=start_index )

        Button(self.root, text="Background Color", font=self.fonts.font_1, bg="SeaGreen3", width=70, height=1).grid(
            row=2, column=1, sticky="nw", padx=10, pady=10)

        Button(self.root, text="Go Back", font=self.fonts.font_1, bg="SeaGreen3", command=self.create_main_menu, width=70, height=1).grid(
            row=3, column=1, sticky="nw", padx=10, pady=10)

    def start_quiz(self):
        MathWindow(self.root, self.fonts)

if __name__ == "__main__":
    MainWindow()