# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:11:35 2021

@author: josep
"""
from functools import partial
from os import listdir
from os.path import join

import tkinter as tk
from . import Index_page

class Loading_page(tk.Frame):
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFCCCC")
             
        get_img = lambda img_name : join("gui", "media_src", "img", img_name)
        bg_im = tk.PhotoImage(file=get_img("loading.pgm"))
        
        tk.Label(master=self, image=bg_im).grid(row=1, column=1)
        
