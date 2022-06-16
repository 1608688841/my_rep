import tkinter as tk
import json

import window_inter
import button

 
 
class Rank:
    def __init__(self, parent_window, s):
        self.s = s
        self.window = tk.Toplevel(parent_window)
        window_inter.WindowInter(self.window, '景点热度排行榜', 500, 400, self.s).show()

        self.contains = []
        self.labels = []
 
        self.get_rank()

        self.s = s
 
        # self.window.mainloop()
 
    def get_rank(self):
        """从db中得到排行榜"""
        js = json.dumps(
                {
                    'type': 'get rank',
                }
               )
        # from passinformation import pass_main
        # jk = pass_main(js)
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
 
        if not jd:
            self.contains = ("故宫", "second", "third", "forth", "颐和园")
        
        else:
            self.contains = jd['msg1']
 
        scroll = tk.Scrollbar(self.window)
        scroll.pack(side="right", fill="y")
 
        listbox = tk.Listbox(self.window, yscrollcommand=scroll.set, font=("宋体", 12), width=70)
 
        for i in range(len(self.contains)):
            label = tk.Label(self.window, text=self.contains[i], font=("宋体", 15, "underline"))
            self.labels.append(label)
            listbox.insert("end", "第"+str(i+1)+":"+self.contains[i])
            listbox.insert("end", " ")
 
        listbox.pack(side="left", fill="both")
        scroll.config(command=listbox.yview)