import tkinter.font as tkFont
from tkinter import Image

# font specifications only
# define fonts
fontNum1 = tkFont.Font(family="Agency FB", size=20, weight="bold")
fontNum2 = tkFont.Font(family="Agency FB", size=30, weight="bold")
fontNum3 = tkFont.Font(family="Arial", size=11, weight="bold")
fontNum4 = tkFont.Font(family="Cooper Black", size=18, weight='normal')

# image paths only
icon_path = "assets/images/Linux_logo.png"
gif_file = "assets/images/giphy3.1.gif"
info = Image.open(gif_file)
frames = info.n_frames  # number of frames
button_image_path = "assets/images/printer.png"
quit_image_path = "assets/images/quit button.png"
append_image_path = "assets/images/append.png"

# data
purchase_list = ['Tables', 'Balloons', 'Party Hats', 'Snacks', 'Drinks', 'Serving Bowls']
counters = {'total_entries': 0, 'name_count': 0}
Items_details = []
