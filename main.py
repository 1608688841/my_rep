import tkinter as tk
import socket
import json

import mainPage
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.102', 8888))
window = tk.Tk()
mainPage.MainPage(window, s)
