from tkinter import *
import tkinter.font as tkFont
import pygame


def setup_main_window_widgets():
    Button(frame_2, text="Setting", font = font_1).grid(row = 0, column = 0, padx=250, pady=70)
    Button(frame_2, text="Records", font = font_1).grid(row = 1, column = 0)
    Button(frame_2, text="Quit", font = font_1, command = quit).grid(row = 0, column = 1)
    Button(frame_2, text="Start", font = font_1).grid(row = 1, column = 1)


def main():
    global frame_1, frame_2, font_1, font_2, font_3, font_4
    root = Tk()
    root.geometry("1280x720")
    root.title("Math Exploration")

    # define fonts
    font_1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
    font_2 = tkFont.Font(family="Agency FB", size=30, weight="bold")
    font_3 = tkFont.Font(family="Arial", size=11, weight="bold")
    font_4 = tkFont.Font(family="Cooper Black", size=18, weight='normal')

    frame_1 = Frame(root, bg= "#e9c46a")
    frame_2 = Frame(root, bg = "#f4a261")
    frame_1.place(relheight=0.5, relwidth=1, rely=0)
    frame_2.place(relheight=0.5, relwidth=1, rely=0.5)

    setup_main_window_widgets()


    root.mainloop()

if __name__ == "__main__":
    main()
