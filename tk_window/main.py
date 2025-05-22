import os
import random
import tkinter.font as tkFont
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image

from utilities import *
from core import *
from constants import *

def main():
    root = Tk()
    root.geometry("750x650")
    root.title("*" * 50 + "Party Purchase" + "*" * 50)
    root.configure(bg='lightblue')

    # Set the window icon
    icon = PhotoImage(file=icon_path)
    root.iconphoto(False, icon)

    # import gif image
    info = Image.open(gif_file)
    frames = info.n_frames  # number of frames

    # Start the GUI
    setup_widgets()
    gif_image()

    messagebox.showinfo(title="Tips(1/2):", message="To record purchases by using this program, input all the required"
                                                    " information, then click the button 'Submit'. To print"
                                                    " the information, please click the button 'Details Window. ")
    messagebox.showinfo(title="Tips(2/2):", message="Having trouble with thinking about receipt numbers all day? "
                                                    "You can actually generate a random receipt number by click the"
                                                    " button 'Random Number' beside 'Receipt Number' entry box. ")

    root.mainloop()

main()