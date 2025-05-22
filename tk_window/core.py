import os
import random
import tkinter.font as tkFont
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image

from constants import *
from utilities import *


def check_inputs():
    input_check = 0

    # Check if Name is blank, set error text if blank
    if len(entry_Name.get()) == 0 or len(entry_Name.get()) > 10 or not entry_Name.get().isalpha():
        show_error(entry_Name)
        messagebox.showerror(title="error",
                             message="Name required, name must be consisted by letters and less than 10 letters")
        input_check = 1
    # Check if the combobox is still in default
    if entry_ItemsPurchased.get() == "Please choose an item name. ":
        messagebox.showerror(title="error", message="Choose a PURCHASED ITEM NAME please. ")
        input_check = 1
    # Check the validation of receipt number(range: 0-2000 include 0 & 2000)
    if entry_ReceiptNumber.get().isdigit():
        if int(entry_ReceiptNumber.get()) <= 0 or int(entry_ReceiptNumber.get()) >= 2000:
            show_error(entry_ReceiptNumber)
            messagebox.showerror(title="error",
                                 message="Input a valid RECEIPT NUMBER please. The receipt number should "
                                         "be a integer which greater that 0, less than 2001. ")
            input_check = 1
    else:
        show_error(entry_ReceiptNumber)
        messagebox.showerror(title="error", message="RECEIPT NUMBER should be an integer. ")
        input_check = 1
    # Check that Items Number is not blank and between 0 and 30, set error text if invalid
    if entry_ItemsNumber.get().isdigit():
        if int(entry_ItemsNumber.get()) <= 0 or int(entry_ItemsNumber.get()) > 100:
            show_error(entry_ItemsNumber)
            messagebox.showerror(title="error",
                                 message="RECEIPT NUMBER should be a integer which greater than 0, less than 101. ")
            input_check = 1
    else:
        show_error(entry_ItemsNumber)
        messagebox.showerror(title="error", message="Input a valid RECEIPT NUMBER please. ")
        input_check = 1

    if input_check == 0:
        messagebox.showinfo("Receipt",
                            f"Details appended successfully! Your receipt number is {str(entry_ReceiptNumber.get())}")
        append_item()


def append_item():
    # Append each item to its own area of the list
    Items_details.append(
        [entry_Name.get(), entry_ItemsPurchased.get(), entry_ItemsNumber.get(), entry_ReceiptNumber.get()])
    save_receipt_to_file(entry_ReceiptNumber.get())
    # Clear the entry boxes
    entry_Name.delete(0, 'end')
    entry_ItemsPurchased.delete(0, 'end')
    entry_ReceiptNumber.delete(0, 'end')
    entry_ItemsNumber.delete(0, 'end')
    counters['total_entries'] += 1
    entry_ItemsPurchased.set("Please choose an item name. ")

    print_details.flash()
    try:
        receipt_win.destroy()
        receipt_window()
    except:
        pass


def save_receipt_to_file(receipt_number):
    if not os.path.exists('savedata'):
        os.makedirs('savedata')
    with open(f'savedata/{receipt_number}.txt', 'w') as file:
        file.write(f"Name: {entry_Name.get()}\n")
        file.write(f"Items Hired: {entry_ItemsPurchased.get()}\n")
        file.write(f"Items Number: {entry_ItemsNumber.get()}\n")
        file.write(f"Receipt Number: {entry_ReceiptNumber.get()}\n")


def delete_receipt_file(receipt_number):
    file_path = f'savedata/{receipt_number}.txt'
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_receipt():
    receipt_number = delete_item.get()
    for item in Items_details:
        if item[3] == receipt_number:
            Items_details.remove(item)
            counters['total_entries'] -= 1
            delete_receipt_file(receipt_number)
            delete_item.delete(0, 'end')
            receipt_window()
            return
    messagebox.showerror(title="error", message="Receipt number not found")
    show_error(delete_item)


def receipt_window():
    global receipt_win, bottom
    try:
        receipt_win.destroy()
    except:
        pass

    receipt_win = Toplevel(root)
    receipt_win.geometry("760x670")
    receipt_win.title("Purchase Details Window")
    receipt_win.iconphoto(False, icon)
    receipt_win.configure(bg='IndianRed3')

    name_count = 0
    # Create the column headings with color
    # Bottom Frame
    bottom = Frame(receipt_win, bg='IndianRed3')
    bottom.place(relheight=1, relwidth=1, rely=0)
    Label(bottom, font=fontNum1, text="Row", fg="white", bg="chocolate1", width=4, height=2, relief="ridge", bd=5).grid(
        column=0, row=0)
    Label(bottom, font=fontNum1, text="Name", fg="white", bg="chocolate1", width=18, height=2, relief="ridge",
          bd=5).grid(
        column=1, row=0)
    Label(bottom, font=fontNum1, text="Items Hired", fg="white", bg="chocolate1", width=20, height=2, relief="ridge",
          bd=5).grid(column=2, row=0)
    Label(bottom, font=fontNum1, text="Hired Amount", fg="white", bg="chocolate1", width=14, height=2, relief="ridge",
          bd=5).grid(column=3, row=0)
    Label(bottom, font=fontNum1, text="Receipt Number", fg="white", bg="chocolate1", width=14, height=2, relief="ridge",
          bd=5).grid(column=4, row=0)

    # Add each item in the list into its own row
    for name_count, item in enumerate(Items_details):
        Label(bottom, text=(name_count + 1), relief="sunken", font=fontNum1, fg="black", bg="white").grid(
            column=0, row=name_count + 1, padx=5, pady=5)
        Label(bottom, text=item[0], relief="sunken", font=fontNum1, fg="black", bg="white").grid(
            column=1, row=name_count + 1, padx=5, pady=5)
        Label(bottom, text=item[1], relief="sunken", font=fontNum1, fg="black", bg="white").grid(
            column=2, row=name_count + 1, padx=5, pady=5)
        Label(bottom, text=item[2], relief="sunken", font=fontNum1, fg="black", bg="white").grid(
            column=3, row=name_count + 1, padx=5, pady=5)
        Label(bottom, text=item[3], relief="sunken", font=fontNum1, fg="black", bg="white").grid(
            column=4, row=name_count + 1, padx=5, pady=5)
    counters['name_count'] = name_count


# Random receipt number generator
def random_receipt():
    randNum = random.randint(1, 2000)
    if len(entry_ReceiptNumber.get()) != 0:
        entry_ReceiptNumber.delete(0, "end")
    entry_ReceiptNumber.insert(0, str(randNum))
    entry_ReceiptNumber.configure(bg="white")

# Create the buttons and labels
def setup_widgets():
    #   import images
    button_image = PhotoImage(file=r"images/printer.png")
    quit_image = PhotoImage(file=r"images/quit button.png")
    append_image = PhotoImage(file=r"images/append.png")

    global entry_Name, entry_ReceiptNumber, entry_ItemsNumber, delete_item, entry_ItemsPurchased, middle, bottom, \
        button_pin, print_details, main_f
    # Main columns
    main_f = Frame(root)
    main_f.place(anchor=NW, relx=0, rely=0, relheight=1, relwidth=1)

    # Create two frames to sort out all the widgets: Top one:
    top = (Frame(main_f, bg='yellow'))
    top.place(anchor=NW, rely=0.25, relheight=0.35, relwidth=1)
    # Create all the labels, buttons, and entry boxes. Put them in the correct grid location
    Label(top, text="Name", bg="orange", font=fontNum1).grid(column=0, row=0, padx=20, pady=25, sticky=W)
    Label(top, text="Items Hired", bg="orange", font=fontNum1).grid(column=0, row=1, padx=20, pady=25, sticky=W)
    Label(top, text="Receipt Number", bg="orange", font=fontNum1).grid(column=2, row=0, padx=20, pady=25, sticky=W)
    Button(top, text="Random Number", bg="tomato", bd=5, font=fontNum3, height=1, command=random_receipt).grid(column=5,
                                                                                                               row=0,
                                                                                                               pady=30,
                                                                                                               sticky='NW')
    Label(top, text="Hired Amount", bg="orange", font=fontNum1).grid(column=2, row=1, padx=20, pady=25, sticky=W)

    # Get purchase information from user input
    entry_Name = Entry(top, width=23)
    entry_Name.grid(column=1, row=0, sticky=W)
    entry_ReceiptNumber = Entry(top, width=23)
    entry_ReceiptNumber.grid(column=3, row=0, sticky=W)
    entry_ItemsNumber = Entry(top, width=23)
    entry_ItemsNumber.grid(column=3, row=1, sticky=W)

    # create combobox
    purchase_list = ['Tables', 'Balloons', 'Party Hats', 'Snacks', 'Drinks', 'Serving Bowls']
    entry_ItemsPurchased = Combobox(top, values=purchase_list, state='readonly')
    entry_ItemsPurchased.grid(column=1, row=1, sticky=W)
    entry_ItemsPurchased.set("Please choose an item name. ")

    # Middle Frame:
    middle = Frame(main_f, bg='orange')
    middle.place(relheight=0.4, relwidth=1, rely=0.6)
    button_pin = Button(middle, text="Pin Window", font=fontNum1, width=20, height=1, bg='SeaGreen3', bd=10,
                        relief='raised', command=pin_window, state='normal', compound=LEFT)
    button_pin.grid(column=0, row=0, padx=10, sticky='NW')
    Button(middle, text="Submit", font=fontNum1, width=200, height=60, bg='OliveDrab1', bd=10, relief='raised',
           image=button_image, compound=LEFT, command=check_inputs).grid(column=1, row=0, padx=20, sticky='NW')
    Button(middle, text="QUIT", fg='red', font=fontNum1, width=20, height=1, bg='yellow2', bd=10, relief='raised',
           command=quit).grid(column=2, row=0, padx=10, sticky='NW')
    Button(middle, text="Delete", font=fontNum1, height=1, width=20, command=delete_receipt, bg='red', bd=10).grid(
        column=0, row=1, padx=10, pady=12, sticky=W)
    delete_item = Entry(middle, width=40)
    preview(delete_item)
    delete_item.grid(column=1, row=1, sticky=W)
    print_details = Button(middle, text="Details Window", font=fontNum1, height=1, width=20, bg='PaleGreen2', bd=10,
                           relief='raised',
                           command=receipt_window)
    print_details.grid(column=2, row=1, padx=10, pady=12)

