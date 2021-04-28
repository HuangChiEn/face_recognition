# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:43:08 2021

@author: josep
"""
from os.path import join
from functools import partial

import tkinter as tk
from . import  Register_page, Recognition_page, Gallery_page, History_page, Update_page

class Index_page(tk.Frame):
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFFFCC")
        
        # Fixed the main window during the register phase.
        regis_template = lambda gui_compnt, win : gui_compnt(win)
        regis_compnt = partial(regis_template, win=self)  # main_win
        
        # Build default config and self-define --
        n_btn = 6
        btn_seq = ("text", "image", "compound", "command")
        self.cfg_lst = [ dict.fromkeys(btn_seq) for _ in range(n_btn) ]
        self.__setup_button_cfg()
        
        for cnt, btn_cfg in enumerate(self.cfg_lst):
            # Common setting
            btn_cfg["compound"] = "left"
            
            # Register GUI component and setting config
            btn_compnt = regis_compnt(tk.Button)
            btn_compnt.config(btn_cfg)
            
            # GUI layout
            idx, jdx = divmod(cnt, 2)
            btn_compnt.grid(row=idx, column=jdx, ipadx=5, ipady=5, padx=50, pady=50)
        
        
    def __setup_button_cfg(self):
        get_img = lambda img_name : join("gui", "media_src", "img", img_name)
        # Button 1.
        btn_cfg = self.cfg_lst[0]
        btn_cfg["text"] = "  Face Registration  "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("regist.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(Register_page.Register_page)
        
        # Button 2.
        btn_cfg = self.cfg_lst[1]
        btn_cfg["text"] = "  Face Recognition  " 
        btn_cfg["image"] = tk.PhotoImage(file=get_img("face_recog.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(Recognition_page.Recognition_page)
        
        # Button 3.
        btn_cfg = self.cfg_lst[2]
        btn_cfg["text"] = "   Face Gallery Set   "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("gallery.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(Gallery_page.Gallery_page)
        
        # Button 4.
        btn_cfg = self.cfg_lst[3]
        btn_cfg["text"] = "     Login History     "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("history.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(History_page.History_page)
        
        # Button 5.
        btn_cfg = self.cfg_lst[4]
        btn_cfg["text"] = "     Update System     "
        btn_cfg["image"] =  tk.PhotoImage(file=get_img("update.pgm")).subsample(8, 8)
        btn_cfg["command"] = lambda : self.parent.switch_page(Update_page.Update_page)
        
        # Button 6.
        btn_cfg = self.cfg_lst[5]
        btn_cfg["text"] = "  Quit "
        btn_cfg["image"] =  tk.PhotoImage(file=get_img("quit.pgm")).subsample(2, 2)
        btn_cfg["command"] = lambda : self.parent.destroy()
