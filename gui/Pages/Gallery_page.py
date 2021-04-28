# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:11:35 2021

@author: josep
"""
from functools import partial
from os import listdir

import tkinter as tk
from . import Index_page

class Gallery_page(tk.Frame):
    ##  Gallery set :
    # 1. Check gallery folder list all name of folders on option menu.
    # 2. furture --> connect to database system and show the personal profile.
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFFFCC")
        name_lst = listdir("face_gallery")
        self.setup_UI(name_lst)
        
    def setup_UI(self, name_lst):
        regis_template = lambda gui_compnt, win : gui_compnt(win)
        regis_compnt = partial(regis_template, win=self)  # main_win
        
        for cnt, name in enumerate(name_lst):
            btn_compnt = regis_compnt(tk.Button)
            btn_compnt["text"] = name
            btn_compnt.grid(row=cnt)
        
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page.Index_page)
                    ).grid(row=cnt+1)
