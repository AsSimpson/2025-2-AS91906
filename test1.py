from tkinter import *

def main():
    root = Tk()
    root.title("StringVar Example")
    root.geometry("300x200")

    # Step 1: Create a StringVar to bind the input
    name_var = StringVar()

    # Step 2: Create an Entry that uses textvariable=name_var
    entry = Entry(root, textvariable=name_var, font=("Arial", 14))
    entry.pack(pady=10)

    # Step 3: Create a Label to show the result
    label = Label(root, text="", font=("Arial", 14))
    label.pack(pady=10)

    # Step 4: Function that reads the current value of name_var
    def show_text():
        label.config(text=f"You typed: {name_var.get()}")

    # Step 5: Create a button to trigger reading the variable
    Button(root, text="Submit", command=show_text).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
