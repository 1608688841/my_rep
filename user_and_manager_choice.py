from this import s
import tkinter as tk
import json
import tkinter.messagebox
 
import button
import window_inter
import attractions
import bus_route
import rank
import account
import user_interface

 
 
class Choice:
    def __init__(self, user_name, pw, mode ,s):
        self.s = s

        self.window = tk.Tk()
 
        self.mode = mode  # 0:user mode 1:manager mode
        self.user_name = user_name
        self.pw = pw
        self.account_now = account.Account(self.user_name, self.pw, self.s)
 
        # 用户模式下的变量
        self.see_attract_butt = tk.Button(self.window, text='查看景点')
        self.query_butt = tk.Button(self.window, text='公交路线查询')
        self.rank_butt = tk.Button(self.window, text='排行榜')
 
        self.see_attract_butt.bind('<1>', self.press_see_attract)
        self.query_butt.bind('<1>', self.press_query)
        self.rank_butt.bind('<1>', self.press_rank)
 
        self.menubar = tk.Menu(self.window)
        self.user_info = tk.Menu(self.menubar, tearoff=0)
 
        self.menubar.add_cascade(label='账户', menu=self.user_info)
 
        self.user_info.add_command(label='账户信息', command=self.account_info)
        self.user_info.add_command(label='预约管理', command=self.appoint)
        self.user_info.add_separator()
        self.user_info.add_command(label='退出', command=self.quit)
 
        # 管理员模式下的变量
        self.tip = tk.Label(self.window, text="请选择登入身份:", font=("宋体", 15))
 
        self.user_mode = tk.Button(self.window, text="用户", font=("宋体", 20))
        self.user_mode.bind("<1>", lambda event: self.create_user_page())
 
        self.manager_mode = tk.Button(self.window, text="管理员", font=("宋体", 20))
        self.manager_mode.bind("<1>", lambda event: self.enter_manager_page())
 
        # self.confirm()
 
    def confirm(self):
        if not self.mode:
            self.create_user_page()
 
        else:
            self.create_manager_page()
 
        self.window.mainloop()
 
    def quit(self):
        """退出"""
        warning = tkinter.messagebox.askokcancel('提示', '即将退出系统\n确定要执行此操作吗?')
        if not warning:
            self.create_user_page()
 
        else:
            self.window.destroy()
            user_interface.UserInter(self.s)
 
    """用户 界面"""
 
    def create_user_page(self):
        window_inter.WindowInter(self.window, '欢迎用户 ' + str(self.user_name) + ' 进入系统', 500, 400, self.s).show()
 
        self.tip.place_forget()
        self.user_mode.place_forget()
        self.manager_mode.place_forget()
 
        self.see_attract_butt.place(x=100, y=40)
        self.query_butt.place(x=100, y=140)
        self.rank_butt.place(x=100, y=240)
 
        self.window.config(menu=self.menubar)
 
    """用户 查看景点"""
    def press_see_attract(self, event):
        """查看景点"""
        attract = attractions.Attraction(self.user_name, self.pw, 0, self.window, self.s)
        attract.confirm_view()
 
    """用户 查询公交路线"""
    def press_query(self, event):
        """"查询公交路线"""
        query = bus_route.BusRoute(self.window, self.s)
        query.confirm()
 
    """用户 查看排行榜"""
    def press_rank(self, event):
        """排行榜"""
        # self.window.destroy()
        rank.Rank(self.window, self.s)
 
    """用户 账号信息"""
    def account_info(self):
        """账户信息"""
        print('account_info is clicked')
 
        acc_window = tk.Toplevel(self.window)
        window_inter.WindowInter(acc_window, '账户信息', 500, 400, self.s).show()
 
        tk.Label(acc_window, text='账户名称:', font=("宋体", 15)).grid(row=2, column=1)
        name = tk.Label(acc_window, text=self.user_name, font=("宋体", 15))
        name.grid(row=2, column=3)
 
        tk.Label(acc_window, text='注册时间:', font=("宋体", 15)).grid(row=6, column=1)
        time = self.account_now.get_time()
        time_label = tk.Label(acc_window, text=time, font=("宋体", 15))
        time_label.grid(row=6, column=3)
 
        cancellation = tk.Label(acc_window, text="注销", font=("宋体", 15, "underline"), fg="red")
        cancellation.grid(row=10, column=1)
        cancellation.bind("<1>", lambda event: self.press_cancel())
 
    """用户 注销账号"""
    def press_cancel(self):
        warning = tkinter.messagebox.askokcancel('提示', '账号会被注销\n确定要执行此操作吗?')
 
        if warning:
            self.account_now.cancellation()
            tkinter.messagebox.showinfo('提示', '注销成功')
            self.window.destroy()
            user_interface.UserInter(self.s)
 
    """用户 预约管理"""
    def appoint(self):
        """预约管理"""
        app_window = tk.Toplevel(self.window)
        window_inter.WindowInter(app_window, '预约信息', 500, 400, self.s).show()
        adapt = []
 
        appointments = self.account_now.get_appointment()
        for i in range(len(appointments)):
            tk.Label(app_window, text=appointments[i][0], font=("宋体", 15)).grid(row=i*2, column=1)
            tk.Label(app_window, text=appointments[i][1], font=("宋体", 15)).grid(row=i*2, column=3)
 
            adapt.append(tk.Label(app_window, text='删除', font=('黑体', 16, "underline"), fg="red"))
            adapt[i].grid(row=i*2, column=5)
            adapt[i].bind("<1>", lambda event: self.press_delete_appoint(
                appointments[0][i], appointments[1][i], app_window))

    def press_delete_appoint(self, attr_name, time, window):
        msg = tkinter.messagebox.askokcancel("警告", "确定删除该预约?")
        if msg:
            # 从db中删除景点预约
            account.Account(self.user_name, self.pw, self.s).cancel_appointment(attr_name=attr_name, appoint_time=time)
            tkinter.messagebox.showinfo('提示', '删除成功')
            window.destroy()
            self.appoint()
 
        return "break"

    """管理员 界面"""
 
    def create_manager_page(self):
        window_inter.WindowInter(self.window, '欢迎管理员 ' + str(self.user_name) + ' 进入系统', 500, 400, self.s).show()
 
        self.tip.place(x=40, y=40)
        self.user_mode.place(x=100, y=100)
        self.manager_mode.place(x=200, y=100)
 
    def enter_manager_page(self):
 
        manager_window = tk.Toplevel(self.window)
        window_inter.WindowInter(manager_window, '管理员系统', 500, 400, self.s).show()
 
        manage_attraction = tk.Button(manager_window, text="景点管理", font=("宋体", 15))
        manage_attraction.bind("<1>", lambda event: self.press_manage_attraction())
 
        manage_user = tk.Button(manager_window, text="用户管理", font=("宋体", 15))
        manage_user.bind("<1>", lambda event: self.press_manage_user())
 
        statistical = tk.Button(manager_window, text="景点数据统计", font=("宋体", 15))
        statistical.bind("<1>", lambda event: self.press_statistical(manager_window))
 
        manage_attraction.grid(row=4, column=1)
        manage_user.grid(row=4, column=7)
        statistical.grid(row=4, column=13)
 
    """管理员 景点管理"""
    def press_manage_attraction(self):
        """景点管理"""
        attractions.Attraction(self.user_name, self.pw, 1, self.window, self.s).confirm_view()
 
    """管理员 用户管理"""
    def press_manage_user(self):
        """用户管理"""
        manage_window = tk.Toplevel(self.window)
        window_inter.WindowInter(manage_window, '用户管理', 500, 400, self.s).show()
 
        statistic_butt = tk.Button(manage_window, text='用户统计', font=("宋体", 20))
        statistic_butt.place(x=100, y=40)
        statistic_butt.bind("<1>", lambda event: self.press_statistic_butt(manage_window))
 
        manage_account = tk.Button(manage_window, text='账号管理', font=("宋体", 20))
        manage_account.place(x=100, y=140)
        manage_account.bind("<1>", lambda event: self.press_manage_account(manage_window))
 
    """管理员 用户账号统计"""
    def press_statistic_butt(self, parent_window):
        statistic_window = tk.Toplevel(parent_window)
        window_inter.WindowInter(statistic_window, '账号统计', 500, 400, self.s).show()
 
        # 从db中获得总计用户数量
        js = json.dumps(
                {
                    'type': "get the number of user",
                    'msg1': ' '
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)

        if not jd['type']:
            amount = 100
        
        else:
            amount = jd['msg1']
 
        # 显示近三条注册记录
        js = json.dumps(
                {
                    'type': "get the recent regist user",
                    'msg1': ' '
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)

        if not jd['msg1']:
            accounts = (("张三", "2022.1.1 11:00"),
                    ("李四", "2022.2.2 22:00"),
                    ("王麻子", "2022.3.3 13:00"))
        
        else:
            accounts = jd['msg1']
 
        # 打印滚动信息
        scroll = tk.Scrollbar(statistic_window)
        scroll.pack(side="right", fill="y")
 
        listbox = tk.Listbox(statistic_window, yscrollcommand=scroll.set, font=("楷体", 15), width=70)
 
        listbox.insert("end", '共计用户 '+str(amount)+' 人')
        listbox.insert("end", ' ')
        listbox.insert("end", '最近两条注册记录:')
        for i in range(len(accounts)):
            listbox.insert("end", '用户 '+accounts[i][0]+' 注册时间: '+accounts[i][1])
 
        listbox.pack(side="left", fill="both")
        scroll.config(command=listbox.yview)
 
        return "break"
 
    """管理员 账号管理"""
    def press_manage_account(self, parent_window):
        account_window = tk.Toplevel(parent_window)
        window_inter.WindowInter(account_window, '账号管理', 500, 400, self.s).show()
 
        entry_butt = button.EntryButton(account_window, '用户名: ', None, 60, self.s)
        entry_butt.grid(column=1, row=3)
 
        confirm_butt = tk.Button(account_window, text='确认', font=("黑体", 14))
        confirm_butt.grid(column=4, row=3)
        confirm_butt.bind("<1>", lambda event: self.confirm_the_account(entry_butt, account_window, parent_window))
 
        return "break"
 
    def confirm_the_account(self, entry_butt, window, parent_window):
        warning = tk.Label(window, text='该账号不存在!', font=("黑体", 15), fg='red')
        name = entry_butt.get_contain_immediate()
        account_now = account.Account(name, -1, self.s)
 
        if not account_now.is_in_db():
            warning.place(x=50, y=100)
 
        else:
            warning.place_forget()
            user_name_label = tk.Label(window, text='用户 '+name, font=("楷体", 15))
            user_name_label.place(x=40, y=90)
            user_register_time_label = tk.Label(window, text='注册时间: ' + account_now.get_time(), font=("楷体", 15))
            user_register_time_label.place(x=40, y=130)
 
            cancellation = tk.Label(window, text="注销", font=("黑体", 15, "underline"), fg="red")
            cancellation.place(x=150, y=200)
            cancellation.bind("<1>", lambda event: self.manager_press_cancel(
                name, window, parent_window))
 
        return "break"
 
    """管理员 注销用户账号"""
    def manager_press_cancel(self, name, window, parent_window):
        warning = tkinter.messagebox.askokcancel('提示', '账号会被注销\n确定要执行此操作吗?')
 
        if warning:
            account.Account(name, -1, self.s).cancellation()
 
            tkinter.messagebox.showinfo('提示', '注销成功')
 
            window.destroy()
            # user_name_label.place_forget()
            # user_register_time_label.place_forget()
 
            self.press_manage_account(parent_window)
 
    """管理员 数据统计"""
 
    def press_statistical(self, parent_window):
        """景点数据统计"""
        window = tk.Toplevel(parent_window)
        window_inter.WindowInter(window, '数据统计', 500, 400, self.s).show()
 
        contains = ("区域景点记录", "景点开放情况", "票价统计")
 
        area_attraction = tk.Button(window, text=contains[0], font=("楷体", 20))
        area_attraction.bind("<1>", lambda event: self.show_statistic(contains[0], window))
 
        open_condition = tk.Button(window, text=contains[1], font=("楷体", 20))
        open_condition.bind("<1>", lambda event: self.show_statistic(contains[1], window))
 
        price_of_all = tk.Button(window, text=contains[2], font=("楷体", 20))
        price_of_all.bind("<1>", lambda event: self.show_statistic(contains[2], window))
 
        area_attraction.place(x=40, y=10)
        open_condition.place(x=40, y=100)
        price_of_all.place(x=40, y=200)
 
    def show_statistic(self, title, parent_window):
        window = tk.Toplevel(parent_window)
        window_inter.WindowInter(window, title, 500, 400, self.s).show()
 
        attraction = attractions.Attraction(self.user_name, self.pw, 1, window, self.s)
        attraction.get_attraction_window().withdraw()
 
        # 打印滚动信息
        scroll = tk.Scrollbar(window)
        scroll.pack(side="right", fill="y")
 
        listbox = tk.Listbox(window, yscrollcommand=scroll.set, font=("宋体", 12), width=70)
 
        if title == "区域景点记录":
            """ contains = (("朝阳区", "1234"),
                            ("天河区", "4321"),
                            ("xx区", "1111"))
            """
            details = attraction.get_area_attraction()
            for i in range(len(details)):
                listbox.insert("end", details[i][0]+' : '+details[i][1])
 
        elif title == "景点开放情况":
            """
            contains = ("111", "222")  # 开放,未开放
            """
            details = attraction.get_open_condition()
            listbox.insert("end", "开放景点: "+details[0])
            listbox.insert("end", "未开放景点: " + details[1])
 
        elif title == "票价统计":
            """
            contains = (("0 - 10", "10"),
                    ("10 - 50", "11"),
                    ("50 - 100", "12"),
                    ("100以上", "13"))
            """
            details = attraction.get_price_of_all()
            for i in range(len(details)):
                listbox.insert("end", details[i][0]+' 的景点个数 '+details[i][1])
 
        listbox.pack(side="left", fill="both")
        scroll.config(command=listbox.yview)