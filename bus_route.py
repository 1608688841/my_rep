import tkinter as tk
from typing import Tuple
import json
 
import window_inter
import button
import attractions
 
 
class BusRoute:
    def __init__(self, parent_window, s):
        self.s = s

        self.window = tk.Toplevel(parent_window)
        window_inter.WindowInter(self.window, '查询巴士路线', 500, 400, self.s).show()
 
        self.start = button.EntryButton(self.window, '起始景点:', None, 90, self.s)
        self.start.grid(row=1, column=1)
        self.start_name = self.start.get_contain_immediate()
 
        self.terminal = button.EntryButton(self.window, '终止景点', None, 90, self.s)
        self.terminal.grid(row=3, column=1)
        self.terminal_name = self.terminal.get_contain_immediate()
 
        self.confirm_butt = tk.Button(self.window, text='确认', font=('宋体', 15))
        self.confirm_butt.grid(row=5, column=2)
 
        """
        self.return_butt = tk.Button(self.window, text='返回', font=('宋体', 15))
        self.return_butt.place(x=200, y=300)
        """
 
        self.warning = tk.Label(self.window, text='')
 
    def press_confirm(self, event):
        self.start_name = self.start.get_contain_immediate()
        self.terminal_name = self.terminal.get_contain_immediate()
 
        start_attr = attractions.Attraction(0, 0, 0, self.window, self.s)
        terminal_attr = attractions.Attraction(0, 0, 0, self.window, self.s)
 
        start_attr.get_attraction_window().withdraw()
        terminal_attr.get_attraction_window().withdraw()
 
        if not self.start_name:
            self.warning.grid_forget()
            self.warning.config(text='起始景点名不能为空')
            self.warning.grid(row=1, column=4)
 
        elif not self.terminal_name:
            self.warning.grid_forget()
            self.warning.config(text='终止景点名不能为空')
            self.warning.grid(row=3, column=4)
 
        elif not start_attr.is_in_db(self.start_name):
            self.warning.grid_forget()
            self.warning.config(text='没有该起始景点')
            self.warning.grid(row=1, column=4)
 
        elif not terminal_attr.is_in_db(self.terminal_name):
            self.warning.grid_forget()
            self.warning.config(text='没有该终止景点')
            self.warning.grid(row=3, column=4)
 
        else:
            self.show_route()
 
    def confirm(self):
        self.confirm_butt.bind('<1>', self.press_confirm)
        self.window.mainloop()
 
    def show_route(self):
        # 得到路线
        js = json.dumps(
                {
                    'type': "get route",
                    'msg1': str(self.start_name),
                    'msg2': str(self.terminal_name),
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
 
        if jd['msg2'] == 'False':
            if jd['msg1'] == 'start':
                self.warning.grid_forget()
                self.warning.config(text='该景点不开放')
                self.warning.grid(row=1, column=4)
            
            elif jd['msg1'] == 'end':
                self.warning.grid_forget()
                self.warning.config(text='该景点不开放')
                self.warning.grid(row=3, column=4)
            
        else:

            if not jd['msg1']:
                route = (('故宫', '站一', '站二', '颐和园'),
                    ('故宫', 'first', 'second', 'third', '颐和园'))
            
            else:
                route = jd['msg1']
    
            bus_window = tk.Toplevel(self.window)
            window_inter.WindowInter(bus_window, '景点信息', 500, 400, self.s).show()
    
            # 打印滚动信息
            scroll = tk.Scrollbar(bus_window)
            scroll.pack(side="right", fill="y")
    
            listbox = tk.Listbox(bus_window, yscrollcommand=scroll.set, font=("宋体", 12), width=70)
            num = 0
            count = 1
            for i in route:
                num = 1
                listbox.insert("end", '第'+str(count)+'条路线:')
                count += 1

                listbox.insert("end", '花费:'+str(i['cost'])+'元')
                listbox.insert("end", '总耗时:'+str(i['duration'])+'分钟')
                listbox.insert("end", '步行距离:'+str(i['walking'])+'米')

                num = i['num']

                for j in range(num):
                    listbox.insert("end", '交通工具:'+str(i[str(j)][0]))
                    listbox.insert("end", '起点站:'+str(i[str(j)][1]))
                    listbox.insert("end", '终点站:'+str(i[str(j)][2]))
                    listbox.insert("end", '乘坐时间:'+str(i[str(j)][3]+'分钟'))
                    if j < num-1:
                        listbox.insert("end", '之后换乘:')

                listbox.insert("end", ' ')
    
            listbox.pack(side="left", fill="both")
            scroll.config(command=listbox.yview)