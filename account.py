import time
 
import socket
 
import json
from unicodedata import name
 
 
 
class Account:
 
    def __init__(self, name, pw, s):
        self.s = s

        self.name = name
        
        self.pw = pw # pw == -1 为默认密码
        
        self.time = str("2022.6.6")
        
        self.appointments = []
        
        self.mode = 0
        
    
    
    def get_appointment(self):
    
        """从数据库读出预约信息"""
        
        js = json.dumps(
        
        {
        
            'type': 'get appointment',
            
            'msg1': self.name
        
        }
        
        )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        
        jd = json.loads(jk)
        
        
        if not jd['msg1']:
        
            self.appointments = (('故宫', '2022.03.03'),
                                ('第二个', '2022.02.02'),
                                ('颐和园', '2022.04.04'))
        
        
        else:
        
            self.appointments = jd['msg1']
        
        
        return self.appointments
    
    
    def cancel_appointment(self, attr_name, appoint_time):
    
        # 从db中删除预约
        
        js = json.dumps(
        
        {
        
            'type': 'delete appointment',
            
            'msg1': attr_name,
            'msg2': appoint_time,
            'msg3': self.name
        
        }
        
        )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        
        jd = json.loads(jk)
        
        
        if jd['msg1'] == 'False':
        
            return False
        
        return True
    
    
    def is_in_db(self):
    
        """判断输入的账户是否在数据库中"""
        js = json.dumps(
                {
                    'type': "is account in db",
                    'msg1': str(self.name),
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
        
        
        if jd['msg1'] == 'True':
            return True

        else:
            return False
        
        
    def is_manager(self):
        
        """判断该账户是否为管理员"""
        
        js = json.dumps(
        
        {
        
        'type': 'is manager',
        
        'msg1': self.name
        
        }
        
        )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        
        jd = json.loads(jk)
        
        
        if jd['msg1'] == 'False':
        
            return False
        
        
        return True
    
    
    def create_account(self):
    
        """将账户加入数据库"""
        
        js = json.dumps(
        
        {
        
            'type': 'create account',
            
            'msg1': self.name,
            
            'msg2': self.pw
        
        }
        
        )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        
        jd = json.loads(jk)
        
        if jd['msg1'] == 'False':
        
            return False
        
        return True
    
    
    def get_name(self):
    
        """获得账户信息"""
        
        return self.name
    
    
    def get_time(self):
    
        """获得注册时间"""
        
        js = json.dumps(
        
        {
        
        'type': 'get register time',
        
        'msg1': self.name
        
        }
        
        )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        
        jd = json.loads(jk)
        
        
        if jd:
        
            self.time = jd['msg1']
        
        
        return self.time
    
    
    def cancellation(self):
    
        """账户从数据库中注销"""
        
        js = json.dumps(
                {
                    'type': "delete",
                    'msg1': str(self.name)
                }
            )
        self.s.send(js.encode())
        while (True):
            jk = self.s.recv(2014).decode()
            if jk:
                break
        jd = json.loads(jk)
        
        if jd['msg1'] == 'False':
        
            return False
        
        else:
        
            return True
    
    
    def is_pw_correct(self):
    
        """判断密码是否正确"""
        
        if self.jd['msg1']=='False' and self.jd['msg2']=='密码错误':
        
            return False
        
        elif self.jd['msg1']=="True" and self.jd['msg2']=="登陆成功":
        
            return True