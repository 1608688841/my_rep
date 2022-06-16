import tkinter as tk

import user_interface
import window_inter
 
 
class MainPage:
    def __init__(self, window, s):
        self.s = s

        self.window = window
        window_inter.WindowInter(self.window, '主界面', 500, 400, self.s).show()
 
        self.com = tk.Label(
            self.window, text='欢迎来到\n\n北京市景点公交导览系统', bg='gray', font=('楷体', 20), padx=20, pady=10, relief="ridge")
        self.com.place(x=70, y=10)
        self.begin_but()
 
        self.window.mainloop()
 
    def begin(self):
        self.window.destroy()
        user_interface.UserInter(self.s)
 
    def begin_but(self):
        begin_but = tk.Button(self.window, text='点击开始', command=self.begin, font=('黑体', 20))
        begin_but.place(x=165, y=200)