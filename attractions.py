from cgitb import text
import tkinter as tk
import tkinter.messagebox
import json

import window_inter
import button
import account

 
class Attraction:
    def __init__(self, user_name, pw, mode, parent_window, s):
        self.s = s

        self.window = tk.Toplevel(parent_window)
        # self.window.withdraw()
 
        self.user_name = user_name
        self.pw = pw
        self.account_now = account.Account(self.user_name, self.pw, self.s)
        self.mode = mode  # 0:user mode 1:manager mode
 
        self.attr_name = ' '
        self.confirm_butt = tk.Button(self.window, text='确定')
        self.selection = button.EntryButton(self.window, '景点名称:', None, 60, self.s)
 
        # 用户模式下的变量
        self.details = ("景点名称", "景点描述", "票价", "开放情况", "景点热度")

        # 推荐的十个景点
        self.recommend_butt = []
        self.recommend = []
 
        # 管理员模式下的变量
        self.details_for_manager = ("景点地址", "景点描述", "票价", "开放情况", "景点搜索量")

        # self.find_butt = button.EntryButton(self.window, '景点名:', None, 60)
        self.find_attraction_for_manager = tk.Button(self.window, text="查询景点", font=("宋体", 15))
        self.find_attraction_for_manager.bind("<1>", lambda event: self.press_find_attraction_for_manager())
 
        self.adapt_attraction = tk.Button(self.window, text="景点修改", font=("宋体", 15))
        self.adapt_attraction.bind("<1>", lambda event: self.press_adapt_attraction())
 
        self.get_appointment = tk.Button(self.window, text="预约记录", font=("宋体", 15))
        self.get_appointment.bind("<1>", lambda event: self.press_get_appointment())
 
        self.delete_butt = tk.Button(self.window, text="删除", font=("黑体", 15))
 
        self.insert_butt = tk.Button(self.window, text="添加", font=("黑体", 15))
        self.insert_butt.bind("<1>", lambda event: self.press_insert())
 
        # self.confirm_view()
 
    def get_attraction_window(self):
        return self.window
 
    def confirm_view(self):
        # self.rank_butt.bind('<1>', self.press_rank)
 
        if not self.mode:
            self.view_for_user()
 
        else:
            self.view_for_manager()
 
        # self.window.mainloop()
 
    def is_in_db(self, attr_name):
        # 判断景点是否在db中
 
        js = json.dumps(
                {
                    'type': 'is attraction in db',
                    'msg1': attr_name
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
 
        if jd['msg1'] =='True':
            return True
        
        else:
            return False
 
    def view_for_user(self):
        window_inter.WindowInter(self.window, '查看景点', 500, 400, self.s).show()
        self.selection.grid(row=1, column=1)
 
        self.confirm_butt.bind('<1>', lambda event: self.find_attraction(self.attr_name))
        self.confirm_butt.grid(row=1, column=3)
 
        self.set_recommend()
 
    def view_for_manager(self):
        # 清除别的按钮
        self.selection.grid_forget()
        self.confirm_butt.grid_forget()
        self.delete_butt.grid_forget()
        self.insert_butt.grid_forget()
 
        window_inter.WindowInter(self.window, '管理景点', 500, 400, self.s).show()
 
        self.find_attraction_for_manager.grid(row=1, column=1)
        self.adapt_attraction.grid(row=1, column=3)
        self.get_appointment.grid(row=1, column=5)
 
    """管理员 景点改查"""
 
    def press_find_attraction_for_manager(self):
        # 清除别的按钮
        self.selection.grid_forget()
        self.confirm_butt.grid_forget()
        self.delete_butt.grid_forget()
        self.insert_butt.grid_forget()
 
        self.selection.grid(row=3, column=1)
 
        self.confirm_butt.bind("<1>", lambda event: self.find_attraction(''))
        self.confirm_butt.grid(row=1, column=4)
 
    """用户 推荐景点"""
    def set_recommend(self):
        # 应从db中取值
        js = json.dumps(
                {
                    'type': 'get recommend',
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
        recommend = jd['msg1']
        if not recommend:
            self.recommend = ('故宫', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        else:
            self.recommend = recommend
 
        row = 5
        column = 0
 
        for i in range(10):
            attract_label = tk.Label(self.window, text=self.recommend[i], font=('宋体', 10, "underline"))
            attract_label.grid(row=row, column=column)
 
            self.recommend_butt.append(attract_label)
            # self.recommend_butt[i].bind('<1>', lambda event: self.press_commend())
 
            column  += 1

            if i == 4:
                row += 1
                column = 0
 
        self.recommend_butt[0].bind('<1>', lambda event: self.find_attraction(self.recommend[0]))
        self.recommend_butt[1].bind('<1>', lambda event: self.find_attraction(self.recommend[1]))
        self.recommend_butt[2].bind('<1>', lambda event: self.find_attraction(self.recommend[2]))
        self.recommend_butt[3].bind('<1>', lambda event: self.find_attraction(self.recommend[3]))
        self.recommend_butt[4].bind('<1>', lambda event: self.find_attraction(self.recommend[4]))
        self.recommend_butt[5].bind('<1>', lambda event: self.find_attraction(self.recommend[5]))
        self.recommend_butt[6].bind('<1>', lambda event: self.find_attraction(self.recommend[6]))
        self.recommend_butt[7].bind('<1>', lambda event: self.find_attraction(self.recommend[7]))
        self.recommend_butt[8].bind('<1>', lambda event: self.find_attraction(self.recommend[8]))
        self.recommend_butt[9].bind('<1>', lambda event: self.find_attraction(self.recommend[9]))
 
    """管理员 用户 景点信息查看"""
    def find_attraction(self, attr_name):
        self.attr_name = self.selection.get_contain_immediate()
        if self.attr_name:
            attr_name = self.attr_name

        if not self.is_in_db(attr_name):
            tkinter.messagebox.showwarning('警告','没有该景点!')

        else:
            # 在db中找到景点
            js = json.dumps(
                    {
                        'type': 'find attraction',
                        'msg1': attr_name
                    }
                )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
    
            if not jd:
                scription = 'good'
                price = 1.2
                is_open = True
                heat = 'very'
                search_count = 233
    
            else:
                scription = jd['scription']
                price = jd['price']
                is_open = jd['is_open']
                heat = jd['heat']
                search_count = jd['search_count']
    
            # 输出信息
            attr_window = tk.Toplevel(self.window)
            adapt_0 = tk.Label(attr_window, text='修改', font=('宋体', 16, "underline"), fg="red")
            adapt_1 = tk.Label(attr_window, text='修改', font=('宋体', 16, "underline"), fg="red")
            adapt_2 = tk.Label(attr_window, text='修改', font=('宋体', 16, "underline"), fg="red")
            adapt_3 = tk.Label(attr_window, text='修改', font=('宋体', 16, "underline"), fg="red")
            adapt_4 = tk.Label(attr_window, text='修改', font=('宋体', 16, "underline"), fg="red")
            adapt = (adapt_0, adapt_1, adapt_2, adapt_3, adapt_4)
            contains = []
    
            window_inter.WindowInter(attr_window, '景点信息', 500, 400, self.s).show()
    
            # 显示景点名称
            tk.Label(attr_window, text='景点名称:', font=('宋体', 16)).grid(column=0, row=0)
            contain_0 = tk.Label(attr_window, text=str(attr_name), font=('宋体', 16))
            contain_0.grid(column=1, row=0)
            contains.append(contain_0)
    
            if self.mode:
                adapt[0].grid(row=0, column=6)
                adapt[0].bind("<1>", lambda event: self.press_adapt("景点名称", attr_window, adapts=adapt, contains=contains))
    
            # 显示景点描述
            tk.Label(attr_window, text='景点描述:', font=('宋体', 16)).grid(column=0, row=2)
            contain_1 = tk.Label(attr_window, text=scription, font=('宋体', 16), wraplength = 120, justify = 'left')
            contain_1.grid(column=1, row=2)
            contains.append(contain_1)
    
            if self.mode:
                adapt[1].grid(row=2, column=6)
                adapt[1].bind("<1>", lambda event: self.press_adapt("景点描述", attr_window, adapts=adapt, contains=contains))
    
            # 显示景点票价
            tk.Label(attr_window, text='票价:', font=('宋体', 16)).grid(column=0, row=4)
            contain_2 = tk.Label(attr_window, text=str(price), font=('宋体', 16))
            contain_2.grid(column=1, row=4)
            contains.append(contain_2)
    
            if self.mode:
                adapt[2].grid(row=4, column=6)
                adapt[2].bind("<1>", lambda event: self.press_adapt("票价", attr_window, adapts=adapt, contains=contains))
    
            # 显示景点开放情况
            tk.Label(attr_window, text='开放情况:', font=('宋体', 16)).grid(column=0, row=6)
            if is_open:
                contain_3 = tk.Label(attr_window, text='The attraction is open now', font=('宋体', 16))
                contain_3.grid(column=1, row=6)
                contains.append(contain_3)
            else:
                contain_3 = tk.Label(attr_window, text='The attraction is close now', font=('宋体', 16))
                contain_3.grid(column=1, row=6)
                contains.append(contain_3)

            if self.mode:
                adapt[3].grid(row=6, column=6)
                adapt[3].bind("<1>", lambda event: self.press_adapt("开放情况", attr_window, adapts=adapt, contains=contains))
    
            # 显示景点热度
            if not self.mode:
                tk.Label(attr_window, text='景点热度:', font=('宋体', 16)).grid(column=0, row=8)
                contain_4 = tk.Label(attr_window, text=heat, font=('宋体', 16))
                contain_4.grid(column=1, row=8)
                contains.append(contain_4)
    
            else:
                tk.Label(attr_window, text='景点搜索量:', font=('宋体', 16)).grid(column=0, row=8)
                contain_4 = tk.Label(attr_window, text=search_count, font=('宋体', 16))
                contain_4.grid(column=1, row=8)
                contains.append(contain_4)

                adapt[4].grid(row=8, column=6)
                adapt[4].bind("<1>", lambda event: self.press_adapt("景点搜索量", attr_window, adapts=adapt, contains=contains))

            if not self.mode:
                    appoint = tk.Label(attr_window, text='预约', font=('宋体', 16, "underline"), fg="red")
                    appoint.grid(row=10, column=1)
                    appoint.bind("<1>", lambda event: self.user_appoint(attr_name, attr_window, appoint))       

    def user_appoint(self, name, window, appoint):
        appoint.grid_forget()

        entry = button.EntryButton(window, '预约时间', None, 60, self.s)
        entry.grid(row=10, column=0)
        time = entry.get_contain_immediate()

        confirm_butt = tk.Button(window, text='确定', font=("黑体", 15))
        confirm_butt.grid(row=10, column=4)
        confirm_butt.bind("<1>", lambda event: self.user_confirm_to_appoint(window, name, time))

    def user_confirm_to_appoint(self, window, name, time):
        #在db中创建预约
        js = json.dumps(
                {
                    'type': 'create appointment',
                    'msg1': name,
                    'msg2': time,
                    'msg3': self.attr_name
                }
               )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)

        msg = tkinter.messagebox.showinfo(title='提示', message='预约创建成功')
        window.destroy()
        self.find_attraction(name)

    def press_adapt(self, name_to_change, window, adapts, contains):
        contain = tk.StringVar()
        adapt = tk.Entry(window, textvariable=contain, font=('宋体', 15))
        confirm_butt = tk.Button(window, text='确定', font=("黑体", 15))
 
        if name_to_change == "景点名称":
            # 修改db
            adapts[0].grid_forget()
            contains[0].grid_forget()
            adapt.grid(column=1, row=0)
            confirm_butt.grid(row=0, column=7)
            confirm_butt.bind("<1>", lambda event: self.confirm_to_adapt(
                name_to_change=name_to_change, attr_name=contain.get(),
                window=window, entry=adapt, confirm=confirm_butt, contains=contains))
 
        elif name_to_change == "景点描述":
            # 修改db
            adapts[1].grid_forget()
            contains[1].grid_forget()
            adapt.grid(column=1, row=2)
            confirm_butt.grid(row=2, column=7)
            confirm_butt.bind("<1>", lambda event: self.confirm_to_adapt(
                name_to_change=name_to_change, attr_name=contain.get(),
                window=window, entry=adapt, confirm=confirm_butt, contains=contains))
 
        elif name_to_change == "票价":
            # 修改db
            adapts[2].grid_forget()
            contains[2].grid_forget()
            adapt.grid(column=1, row=4)
            confirm_butt.grid(row=4, column=7)
            confirm_butt.bind("<1>", lambda event: self.confirm_to_adapt(
                name_to_change=name_to_change, attr_name=contain.get(),
                window=window, entry=adapt, confirm=confirm_butt, contains=contains))
 
        elif name_to_change == "开放情况":
            # 修改db
            adapts[3].grid_forget()
            contains[3].grid_forget()
            adapt.grid(column=1, row=6)
            confirm_butt.grid(row=6, column=7)
            confirm_butt.bind("<1>", lambda event: self.confirm_to_adapt(
                name_to_change=name_to_change, attr_name=contain.get(),
                window=window, entry=adapt, confirm=confirm_butt, contains=contains))
 
        elif name_to_change == "景点搜索量":
            # 修改db
            adapts[4].grid_forget()
            contains[4].grid_forget()
            adapt.grid(column=1, row=8)
            confirm_butt.grid(row=8, column=7)
            confirm_butt.bind("<1>", lambda event: self.confirm_to_adapt(
                name_to_change=name_to_change, attr_name=contain.get(),
                window=window, entry=adapt, confirm=confirm_butt, contains=contains))
 
    def confirm_to_adapt(self, name_to_change, attr_name, window, entry, confirm, contains):
        entry.grid_forget()
        confirm.grid_forget()
 
        adapt_0 = tk.Label(window, text='修改', font=('宋体', 16, "underline"), fg="red")
        adapt_1 = tk.Label(window, text='修改', font=('宋体', 16, "underline"), fg="red")
        adapt_2 = tk.Label(window, text='修改', font=('宋体', 16, "underline"), fg="red")
        adapt_3 = tk.Label(window, text='修改', font=('宋体', 16, "underline"), fg="red")
        adapt_4 = tk.Label(window, text='修改', font=('宋体', 16, "underline"), fg="red")
        adapt = (adapt_0, adapt_1, adapt_2, adapt_3, adapt_4)
 
        if name_to_change == "景点名称":
 
            js = json.dumps(
                {
                    'type': 'adapt name',
                    'msg1': self.attr_name,
                    'msg2': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            self.attr_name = attr_name
 
            contains[0] = tk.Label(window, text=attr_name, font=('宋体', 16))
            contains[0].grid(column=1, row=0)
 
            adapt[0].grid(row=0, column=6)
            adapt[0].bind("<1>", lambda event: self.press_adapt("景点名称", window, adapts=adapt, contains=contains))
 
        elif name_to_change == "景点描述":
 
            js = json.dumps(
                {
                    'type': 'adapt scription',
                    'msg1': self.attr_name,
                    'msg2': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            contains[1] = tk.Label(window, text=attr_name, font=('宋体', 16))
            contains[1].grid(column=1, row=2)
 
            adapt[1].grid(row=2, column=6)
            adapt[1].bind("<1>", lambda event: self.press_adapt("景点描述", window, adapts=adapt, contains=contains))
 
        elif name_to_change == "票价":
 
            js = json.dumps(
                {
                    'type': 'adapt price',
                    'msg1': self.attr_name,
                    'msg2': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            contains[2] = tk.Label(window, text=attr_name, font=('宋体', 16))
            contains[2].grid(column=1, row=4)
 
            adapt[2].grid(row=4, column=6)
            adapt[2].bind("<1>", lambda event: self.press_adapt("票价", window, adapts=adapt, contains=contains))
 
        elif name_to_change == "开放情况":
 
            js = json.dumps(
                {
                    'type': 'adapt open condition',
                    'msg1': self.attr_name,
                    'msg2': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            contains[3] = tk.Label(window, text=attr_name, font=('宋体', 16))
            contains[3].grid(column=1, row=6)
 
            adapt[3].grid(row=6, column=6)
            adapt[3].bind("<1>", lambda event: self.press_adapt("开放情况", window, adapts=adapt, contains=contains))
 
        elif name_to_change == "景点搜索量":
 
            js = json.dumps(
                {
                    'type': 'adapt search count',
                    'msg1': self.attr_name,
                    'msg2': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            contains[4] = tk.Label(window, text=attr_name, font=('宋体', 16))
            contains[4].grid(column=1, row=8)
 
            adapt[4].grid(row=8, column=6)
            adapt[4].bind("<1>", lambda event: self.press_adapt("景点搜索量", window, adapts=adapt, contains=contains))
 
    """管理员 景点增删"""
 
    def press_adapt_attraction(self):
        # 清除别的按钮
        self.selection.grid_forget()
        self.confirm_butt.grid_forget()
        self.delete_butt.grid_forget()
        self.insert_butt.grid_forget()
 
        self.selection.show(40, 50)
 
        self.confirm_butt.bind("<1>", lambda event: self.adapt())
        self.confirm_butt.grid(row=3, column=5)
 
    def adapt(self):
        # 获得要修改的景点名称
        self.attr_name = self.selection.get_contain_immediate()
 
        if self.is_in_db(self.attr_name):
            self.confirm_butt.grid_forget()
            self.delete_butt.grid_forget()
            self.insert_butt.grid_forget()

            self.delete_butt.bind("<1>", lambda event: self.press_delete())
            self.delete_butt.grid(row=5, column=3)
 
        else:
            self.confirm_butt.grid_forget()
            self.delete_butt.grid_forget()
            self.insert_butt.grid_forget()

            self.insert_butt.grid(row=5, column=3)
            self.insert_butt.bind("<1>", lambda event: self.press_insert())
 
        return "break"
 
    """管理员 景点删除"""
    def press_delete(self):
        if not self.is_in_db(name):
            tkinter.messagebox.showwarning('警告','没有该景点')

        else:
            msg = tkinter.messagebox.askokcancel("警告", "确定删除该景点?")

            if msg:
                # self.confirm_butt.grid_forget()
                self.delete_butt.grid_forget()
                self.insert_butt.grid_forget()

                # 从db中删除景点
                name = self.selection.get_contain_immediate()
                js = json.dumps(
                    {
                        'type': 'delete attraction',
                        'msg1': name
                    }
                )
                self.s.send(js.encode())
                while (True):
                    jk = self.s.recv(2014).decode()
                    if jk:
                        break
                jd = json.loads(jk)
    
                tkinter.messagebox.showinfo('提示', '删除成功')
 
        return "break"
 
    """管理员 景点增加"""
    def press_insert(self):
        msg = tkinter.messagebox.askokcancel("警告", "确定添加该景点?")
        row = 3
        insert_entry = []  # 获取修改内容
        if msg:
            self.confirm_butt.grid_forget()
            self.delete_butt.grid_forget()
            self.insert_butt.grid_forget()
 
            for i in self.details_for_manager:
                butt = button.EntryButton(self.window, i+':', None, 60, self.s)
                butt.grid(row=row, column=0)
                insert_entry.append(butt)
 
                row += 1
            self.confirm_butt.grid(row=row+1, column=3)
            self.confirm_butt.bind("<1>", lambda event: self.confirm_to_insert(insert_entry))
        return "break"
 
    def confirm_to_insert(self, insert_entry):
        insert_detail = []
        tkinter.messagebox.showinfo(title='提示', message='创建成功')
        for i in insert_entry:
            insert_detail.append(i.get_contain_immediate())
            i.forget()
        # 从db中添加该景点
        js = json.dumps(
                {
                    'type': 'insert attraction',
                    'msg1': self.name,
                    'msg2': insert_detail
                }
               )
        self.s.send(js.encode())
        while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
        jd = json.loads(jk)
 
        self.view_for_manager()
        return "break"
 
    """管理员 景点预约记录"""
 
    def press_get_appointment(self):
        # 清除别的按钮
        self.selection.grid_forget()
        self.confirm_butt.grid_forget()
        self.delete_butt.grid_forget()
        self.insert_butt.grid_forget()
 
        self.selection.show(40, 40)
        self.confirm_butt.grid(row=3, column=5)
 
        attr_name = self.selection.get_contain_immediate()
        self.confirm_butt.bind("<1>", lambda event: self.confirm_to_appoint(attr_name, self.is_in_db(attr_name)))
 
    def confirm_to_appoint(self, attr_name, is_in_db):
        warning = tk.Label(self.window, text='没有该景点!', font=("黑体", 15, "underline"), fg="red")
        if not is_in_db:
            warning.place(x=200, y=100)
 
        else:
            warning.place_forget()
            appoint_window = tk.Toplevel(self.window)
            window_inter.WindowInter(appoint_window, '景点'+str(attr_name)+'预约记录', 500, 400, self.s).show()
 
            # 从db中调出预约信息
 
            js = json.dumps(
                {
                    'type': 'get appointment of attraction',
                    'msg1': attr_name
                }
               )
            self.s.send(js.encode())
            while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
            jd = json.loads(jk)
 
            if not jd['msg1']:
                appoint_name = ("张三", "李四", "王麻子")
                appoint_time = ("2022.1.1", "2022.2.2", "2022.3.3")
                # appoint_attraction = ("颐和园", "故宫", "长城")
 
            else:
                appoint_name = jd['msg1']
                appoint_time = jd['msg2']
 
            adapt_appoint = []
 
            for i in range(len(appoint_name)):
                tk.Label(appoint_window, text=appoint_name[i], font=("宋体", 15)).grid(row=i * 2, column=1)
                tk.Label(appoint_window, text=appoint_time[i], font=("宋体", 15)).grid(row=i * 2, column=3)
                # tk.Label(appoint_window, text=appoint_attraction[i], font=("宋体", 15)).grid(row=i * 2, column=3)
 
                adapt_appoint.append(tk.Label(appoint_window, text='取消预约', font=("黑体", 15, "underline"), fg="red"))
                adapt_appoint[i].grid(row=i * 2, column=5)
                adapt_appoint[i].bind(
                    "<1>", lambda event: self.confirm_to_cancel_appoint(
                        appoint_name, appoint_time, appoint_window, attr_name))
        return "break"
 
    def confirm_to_cancel_appoint(self, appoint_name, appoint_time, window, attr_name):
        msg = tkinter.messagebox.askokcancel("警告", "确定删除该预约?")
        if msg:
            # 从db中删除景点预约
            account.Account(self.user_name, self.pw, self.s).cancel_appointment(attr_name=attr_name, appoint_time=appoint_time)
            tkinter.messagebox.showinfo('提示', '删除成功')
            self.confirm_to_appoint(attr_name, 1)
            window.destroy()
        return "break"
 
    """管理员 数据统计"""
 
    """管理员 区域景点记录"""
    def get_area_attraction(self):
        # 从db中获得景点记录
        js = json.dumps(
                {
                    'type': 'get area attraction'
                }
               )
        self.s.send(js.encode())
        while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
        jd = json.loads(jk)
 
        if not jd['msg1']:
            contains = (("朝阳区", "1234"),
                        ("天河区", "4321"),
                        ("xx区", "1111"))
 
        else:
            contains = jd['msg1']
 
        return contains
 
    """管理员 开放情况"""
    def get_open_condition(self):
        # 从db中获得开放记录
        js = json.dumps(
                {
                    'type': 'get open condition of all'
                }
               )
        self.s.send(js.encode())
        while (True):
                jk = self.s.recv(2014).decode()
                if jk:
                    break
        jd = json.loads(jk)
 
        if not jd['msg1']:
            contains = ("111", "222")  # 开放,未开放
 
        else:
            contains = jd['msg1']
 
        return contains
 
    """管理员 所有景点票价"""
    def get_price_of_all(self):
        # 从db中获得票价记录
        js = json.dumps(
                {
                    'type': 'get price of all'
                }
               )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
 
        if not jd['msg1']:
            contains = (("0 - 10", "10"),
                        ("10 - 50", "11"),
                        ("50 - 100", "12"),
                        ("100以上", "13"))
 
        else:
            contains = jd['msg1']
 
        return contains
 