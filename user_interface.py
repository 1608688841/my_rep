import tkinter as tk

import user_login
import user_regist
import window_inter
 
 
class UserInter:
    def __init__(self, s):
        self.s = s

        self.window = tk.Tk()
        window_inter.WindowInter(self.window, '北京市景点公交导览系统登录', 500, 400, self.s).show()
 
        login_but = tk.Button(
            self.window, text='登录', command=self.login, padx=3, pady=2, font=('黑体', 20))
        regist_but = tk.Button(
            self.window, text='注册', command=self.regist, padx=3, pady=2, font=('黑体', 20))
 
        login_but.place(x=160, y=100)
        regist_but.place(x=160, y=200)
 
        self.window.mainloop()
 
    def login(self):
        self.window.destroy()
        login = user_login.LogPage(self.s)
        login.confirm()
 
    def regist(self):
        self.window.destroy()
        register = user_regist.RegistPage(self.s)
        register.confirm()