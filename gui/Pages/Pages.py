# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:43:08 2021

@author: josep
"""
import tkinter as tk

from os.path import join
from os import makedirs, listdir
from functools import partial

## should replace to relatively path with face_recognizer package
import sys
#sys.path.append(join("face_recognizer", "recognition"))
#from recognizer import Face_Recognizer

# new package for replace the recognizer..
sys.path.append(join("face_recognizer", "detector"))
from detector import Face_Detector

sys.path.append(join("face_recognizer", "classifier"))
from classifier import Face_Classifier


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
        btn_cfg["command"] = lambda: self.parent.switch_page(Register_page)
        
        # Button 2.
        btn_cfg = self.cfg_lst[1]
        btn_cfg["text"] = "  Face Recognition  " 
        btn_cfg["image"] = tk.PhotoImage(file=get_img("face_recog.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(Recognition_page)
        
        # Button 3.
        btn_cfg = self.cfg_lst[2]
        btn_cfg["text"] = "   Face Gallery Set   "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("gallery.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(Gallery_page)
        
        # Button 4.
        btn_cfg = self.cfg_lst[3]
        btn_cfg["text"] = "     Login History     "
        btn_cfg["image"] = tk.PhotoImage(file=get_img("history.pgm"))
        btn_cfg["command"] = lambda: self.parent.switch_page(History_page)
        
        # Button 5.
        btn_cfg = self.cfg_lst[4]
        btn_cfg["text"] = "     Update System     "
        btn_cfg["image"] =  tk.PhotoImage(file=get_img("update.pgm")).subsample(8, 8)
        btn_cfg["command"] = lambda : self.parent.switch_page(Update_page)
        
        # Button 6.
        btn_cfg = self.cfg_lst[5]
        btn_cfg["text"] = "  Quit "
        btn_cfg["image"] =  tk.PhotoImage(file=get_img("quit.pgm")).subsample(2, 2)
        btn_cfg["command"] = lambda : self.parent.destroy()
        


class Register_page(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#66CCFF")
        self.face_detector = Face_Detector() 
        self.setup_UI()
        
    def setup_UI(self):
        pad_opt = {'ipadx':5, 'ipady':5, 'padx':5, 'pady':5}
        
        tk.Label(master=self, text="Register Name").grid(row=0, column=0, **pad_opt)
        regist_name = tk.StringVar()
        tk.Entry(master=self, textvariable=regist_name).grid(row=0, column=1, **pad_opt)
        
        btn = tk.Button(text="submit", master=self,
                  command=lambda : self.register_face(regist_name.get()))
        btn.grid(row=1, column=0, columnspan=2, **pad_opt)
        
        btn = tk.Button(text="back to menu", master=self,
                  command=lambda : self.parent.switch_page(Index_page))
        btn.grid(row=2, column=0, columnspan=2, **pad_opt)
        
        
    def register_face(self, name='Unknown', face_img_dir='face_gallery'):
        save_dir = join(face_img_dir, name)
        makedirs(save_dir, exist_ok=True)
        self.face_detector.detection(save_dir)
        

class Recognition_page(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFFFCC")
        # prepare recognizer sub_module
        self.detector = Face_Detector() 
        self.classifier = Face_Classifier()
        self.setup_UI()
        
    def setup_UI(self):
        recg_btn = tk.Button(text="recognition", master=self,
                  command=lambda : self.face_recognition())
        recg_btn.grid(row=0, column=0)
        recg_btn = tk.Button(text="back to menu", master=self,
                  command=lambda : self.parent.switch_page(Index_page))
        recg_btn.grid(row=1, column=0)
        
    def face_recognition(self):
        self.detector.recog_detect(self.classifier)


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
        
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page)
                    ).grid(row=cnt+1)
     
        
class History_page(tk.Frame):
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFFFCC")
        self.setup_UI()
        
    def setup_UI(self):
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page)
                    ).grid(row=0)
        

class Update_page(tk.Frame):
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FF6666")
        self.cls = Face_Classifier()
        self.setup_UI()

    def setup_UI(self):
        pad_opt = {'ipadx':5, 'ipady':5, 'padx':5, 'pady':5}
        
        tk.Label(master=self, text="num of limit for training").grid(row=0, column=0, columnspan=2, **pad_opt)
        lim_num = tk.StringVar()
        tk.Entry(master=self, textvariable=lim_num).grid(row=1, column=0, columnspan=2,**pad_opt)
        
        btn = tk.Button(text="update system", master=self,
                  command=lambda : self.cls.update_classfier(lim_num.get()))
        btn.grid(row=2, column=0, columnspan=2, **pad_opt)
        
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page)
                    ).grid(row=3, column=0, columnspan=2, **pad_opt)

