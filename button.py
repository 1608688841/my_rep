import tkinter as tk
 
 
class EntryButton:
    def __init__(self, window, text, show_type, distance, s):
        self.s = s

        self.text = text
        self.showType = show_type
        self.distance = distance
 
        self.contain = tk.StringVar()
        self.name = tk.Label(window, text=self.text)
        self.contain = tk.Entry(
            window, show=self.showType, textvariable=self.contain, font=('宋体', 14))
 
    def show(self, x, y):
        self.name.place(x=x, y=y)
        self.contain.place(x=x + self.distance, y=y)
 
    def get_contain(self):
        return self.contain.get()
 
    def get_contain_immediate(self):
        return self.contain.get()
 
    def forget(self):
        self.name.place_forget()
        self.contain.place_forget()

    def grid(self, row, column):
            self.name.grid(row=row, column=column)
            self.contain.grid(row=row, column=column+1)

    def grid_forget(self):
        self.name.grid_forget()
        self.contain.grid_forget()
