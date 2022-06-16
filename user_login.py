import tkinter as tk
import json
import tkinter.messagebox

import button
import user_interface
import window_inter
import user_and_manager_choice
import account

 
 
class LogPage:
    """"用户登录"""
    def __init__(self, s):
        self.s = s

        self.window = tk.Tk()
        window_inter.WindowInter(self.window, '用户登录', 500, 400, self.s).show()
 
        self.user = button.EntryButton(self.window, '用户名', None, 60, self.s)
        self.user.show(40, 100)
 
        self.pw = button.EntryButton(self.window, '密码', '*', 60, self.s)
        self.pw.show(40, 180)
 
        self.confirm_butt = tk.Button(self.window, text='确认', font=15)
        self.confirm_butt.place(x=100, y=240)
 
        self.return_butt = tk.Button(self.window, text='返回', font=15)
        self.return_butt.place(x=220, y=240)
 
        self.warning = tk.Label(self.window, text='')
 
    def press_confirm(self, event):
        account_now = account.Account(self.user.get_contain(), self.pw.get_contain(), self.s)
            
        if not self.user.get_contain():
            self.warning.config(text='账号不能为空')
            self.warning.place(x=330, y=90)
 
        elif not self.pw.get_contain():
            self.warning.config(text='密码不能为空')
            self.warning.place(x=330, y=180)

        js = json.dumps(
                {
                    'type': 'login',
                    'msg1': self.user.get_contain_immediate(),
                    'msg2': self.pw.get_contain_immediate()
                }
               )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)

        if jd['msg1'] == 'False':
            tkinter.messagebox.showwarning('警告',jd['msg2'])
 
        elif jd['msg3'] == '用户':
            user_name = self.user.get_contain()
            pw = self.pw.get_contain()
            self.window.destroy()
            choice = user_and_manager_choice.Choice(user_name, pw, 0, self.s).confirm()
 
        elif jd['msg3'] == '管理员':
            user_name = self.user.get_contain()
            pw = self.pw.get_contain()
            self.window.destroy()
            choice = user_and_manager_choice.Choice(user_name, pw, 1, self.s).confirm()
 
        return "break"
 
    def press_return(self, event):
        self.window.destroy()
        user_interface.UserInter(self.s)
 
        return "break"
 
    def confirm(self):
        self.confirm_butt.bind('<1>', self.press_confirm)
        self.return_butt.bind('<1>', self.press_return)
 
        self.window.mainloop()