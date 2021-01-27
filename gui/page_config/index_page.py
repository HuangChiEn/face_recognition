# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:43:08 2021

@author: josep
"""

import tkinter as tk

class index_page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        




