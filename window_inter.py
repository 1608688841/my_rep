import tkinter as tk
# from PIL import ImageTk, Image
 
 
class WindowInter:
    def __init__(self, window, title, width, height, s):
        self.s = s
        self.window = window
        self.width = width
        self.height = height
        self.window.title(title)
 
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
 
        # image2 = Image.open(r'C:\Python27\tcl\tk8.5\demos\images\earth.gif')
        # background_image = ImageTk.PhotoImage(image2)
 
        self.left = (screen_width - self.width) / 2
        self.top = (screen_height - self.height) / 2
 
    def show(self):
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, self.left, self.top))
 
 