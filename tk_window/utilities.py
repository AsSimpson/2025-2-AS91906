import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image
from constants import *


def show_error(object_name):
    # Define a function to clear the content of the text widget
    def click(event):
        object_name.delete(0, END)
        object_name.configure(bg="white")
        object_name.unbind('<Button-1>', clicked)

    object_name.configure(bg="firebrick1")
    clicked = object_name.bind('<Button-1>', click)


def preview(widget_name):
    # Define a function to clear the content of the text widget
    def click(event):
        widget_name.delete(0, END)
        widget_name.configure(fg='black')
        widget_name.unbind('<Button-1>', clicked)

    widget_name.configure(fg='red')
    widget_name.insert(0, "Enter Receipt Number here. ")
    clicked = widget_name.bind('<Button-1>', click)

def pin_window(button):
    button = button
    if str(button['bg']) != 'gray':
        root.attributes('-topmost', True)
        button.configure(bg='gray', text="Unpin Window")
    elif str(button['bg']) == 'gray':
        root.attributes('-topmost', False)
        button.configure(bg='SeaGreen3', text="Pin Window")


def animation(current_frame=0):
    global loop, loop_2
    image = photoimage_objects[current_frame]

    gif_label.configure(image=image)

    current_frame += 1

    if current_frame == frames:
        current_frame = 0

    loop = title_frame.after(50, lambda: animation(current_frame))
    # loop_2 = title_frame.after(50, lambda: animation(current_frame))


def gif_image(main_f):
    global title_frame, photoimage_objects, photoimage_objects_2, gif_label, gif_label_2
    title_frame = Frame(main_f, bg='gold2')
    title_frame.place(anchor=NW, relx=0, rely=0, relheight=0.25, relwidth=1)

    photoimage_objects = []
    for i in range(frames):
        obj = PhotoImage(file=gif_file, format=f"gif -index {i}")
        photoimage_objects.append(obj)

    gif_label = Label(title_frame, bg='gold2', image="")
    gif_label.place(x=70, y=0)

    animation(current_frame=0)

