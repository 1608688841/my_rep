import tkinter as tk
import tkinter.messagebox
import json

import button
import user_interface
import window_inter
import account

 
 
class RegistPage:
    def __init__(self, s):
        self.s = s
        self.window = tk.Tk()
        window_inter.WindowInter(self.window, '用户注册', 500, 400, self.s).show()
 
        self.user = button.EntryButton(self.window, '用户名', None, 60, self.s)
        self.user.grid(row=1, column=0)
 
        self.pw_1 = button.EntryButton(self.window, '密码', '*', 55, self.s)
        self.pw_1.grid(row=2, column=0)
 
        self.pw_2 = button.EntryButton(self.window, '确认密码', '*', 70, self.s)
        self.pw_2.grid(row=3, column=0)
 
        self.confirm_butt = tk.Button(self.window, text='确认')
        self.confirm_butt.grid(row=4, column=0)
 
        self.return_butt = tk.Button(self.window, text='返回')
        self.return_butt.grid(row=1, column=1)
 
        self.warning = tk.Label(self.window, text='')
 
        # self.window.mainloop()
 
    def is_correct(self):
        """双重密码确认"""
        if self.pw_1.get_contain() == self.pw_2.get_contain():
            return True
        else:
            return False
 
    def press_confirm(self, event):
        account_now = account.Account(self.user.get_contain(), self.pw_1.get_contain(), self.s)
 
        if self.user.get_contain() == '':
            self.warning.config(text='用户名不能为空')
            self.warning.grid(row=1, column=4)
 
        elif self.pw_1.get_contain() == '':
            self.warning.config(text='密码不能为空')
            self.warning.grid(row=2, column=4)
 
        elif not self.is_correct():
            self.warning.config(text='密码不一致')
            self.warning.grid(row=3, column=4)

        else:

            js = json.dumps(
                    {
                        'type': 'sign',
                        'msg1': self.user.get_contain_immediate(),
                        'msg2': self.pw_1.get_contain_immediate(),
                        'msg3': self.pw_2.get_contain_immediate()
                    }
                )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)

            if jd['msg1'] == 'False' and jd['msg2'] == '用户名重复':
                self.warning.config(text='该账号已存在')
                self.warning.grid(row=1, column=4)
    
            else:
                # account_now.create_account()
                self.warning.place_forget()
                tkinter.messagebox.showinfo(title='提示', message='创建成功')
    
        return "break"
 
    def press_return(self, event):
        self.window.destroy()
        user_interface.UserInter(self.s)
 
        return "break"
 
    def confirm(self):
        self.confirm_butt.bind('<1>', self.press_confirm)
        self.return_butt.bind('<1>', self.press_return)
 
        self.window.mainloop()