# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 09:58:21 2020

@author: josep
"""

from tkinter import W, E, N, S
import tkinter as tk

import os
from os import makedirs
from os.path import join
from functools import partial

import sys
sys.path.append(join("face_recognizer", "detector"))
from detector import Face_Detector

class Recognizer_GUI(object):
    def __init__(self, parent, **kwargs):
        self.root = parent
        self.setup_root_cfg()
        self.setup_UI()
        self.face_detector = Face_Detector()
        
        
    def register_face(self, face_img_dir='', name='Unknown'):
        save_dir = join(face_img_dir, name)
        makedirs(save_dir, exist_ok=True)
        self.face_detector.face_detection(save_dir)
        
    
    def setup_root_cfg(self):
        self.root.title("Face Recognizer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(background='#FFFF99')
        self.root.iconbitmap(os.path.join("gui", "media_src", "icon", "recog_logo.ico"))
        
    def setup_UI(self):
        
        def setup_button_cfg():
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
            btn_cfg["command"] = lambda : self.root.destroy()
            
            
        # set the fundamental geometric manager.
        self.main_frame = tk.Frame(self.root, bg='#FFFFCC')
        self.main_frame.pack(expand=1)
                 
        # Fixed the main window during the register phase. 
        regis_template = lambda gui_compnt, win : gui_compnt(win)
        regis_compnt = partial(regis_template, win=self.main_frame)  # main_win
        
        # Build default config and self-define --
        btn_seq = ("text", "image", "compound", "command")
        self.cfg_lst = [ dict.fromkeys(btn_seq) for _ in range(5) ]
        setup_button_cfg()

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
        

if __name__ == "__main__":
    pass
    #main_win = tk.Tk()
    #Recognizer_GUI(main_win)
    
    # Activate loop for listen event
    #main_win.mainloop()           
