# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:43:08 2021

@author: josep
"""
from tkinter import W, E, N, S
import tkinter as tk

from os.path import join
from os import makedirs
from functools import partial

import sys
sys.path.append(join("face_recognizer", "detector"))
from detector import Face_Detector

class Index_page(tk.Frame):
    
    def __init__(self, parent):
        self.parent = parent
        self.face_detector = Face_Detector()
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg='#FFFFCC')
        
        # Fixed the main window during the register phase. 
        regis_template = lambda gui_compnt, win : gui_compnt(win)
        regis_compnt = partial(regis_template, win=self)  # main_win
        
        # Build default config and self-define --
        btn_seq = ("text", "image", "compound", "command")
        self.cfg_lst = [ dict.fromkeys(btn_seq) for _ in range(5) ]
        self.__setup_button_cfg()
        
        btn_lst = []
        for cnt, btn_cfg in enumerate(self.cfg_lst):
            # Common setting
            btn_cfg["compound"] = "left"
            
            # Register GUI component and setting config
            btn_compnt = regis_compnt(tk.Button)
            btn_compnt.config(btn_cfg)
            
            # GUI layout
            idx, jdx = divmod(cnt, 2)
            if cnt < 5:
                btn_compnt.grid(row=idx, column=jdx, ipadx=5, ipady=5, padx=50, pady=50)
            btn_lst.append(btn_compnt)
            
        btn_lst[-1].grid(row=2, column=0, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=250, pady=50)
        
        
    def register_face(self, face_img_dir='', name='Unknown'):
        save_dir = join(face_img_dir, name)
        makedirs(save_dir, exist_ok=True)
        self.face_detector.face_detection(save_dir)
        
        
    def __setup_button_cfg(self):
        get_img = lambda img_name : join("gui", "media_src", "img", img_name)
        # Button 1.
        btn_cfg = self.cfg_lst[0]
        btn_cfg["text"] = "  Face Registration  "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("regist.pgm"))
        btn_cfg["command"] = self.register_face
        
        # Button 2.
        btn_cfg = self.cfg_lst[1]
        btn_cfg["text"] = "  Face Recognition  " 
        btn_cfg["image"] = tk.PhotoImage(file=get_img("face_recog.pgm"))
        
        # Button 3.
        btn_cfg = self.cfg_lst[2]
        btn_cfg["text"] = "   Face Gallery Set   "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("gallery.pgm"))
        
        # Button 4.
        btn_cfg = self.cfg_lst[3]
        btn_cfg["text"] = "     Login History     "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("history.pgm"))
        
        # Button 5.
        btn_cfg = self.cfg_lst[4]
        btn_cfg["text"] = "  Quit "
        btn_cfg["image"] =  tk.PhotoImage(file=get_img("quit.pgm")).subsample(2, 2)
        btn_cfg["command"] = lambda : self.parent.destroy()

