# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:11:34 2021

@author: josep
"""
from os.path import join
from os import makedirs

## should replace to relatively path with face_recognizer package
import sys
# new package for replace the recognizer..
sys.path.append(join("face_recognizer", "detector"))
from detector import Face_Detector

import tkinter as tk
from . import Index_page       ## Note : directly import prevent circular import problem.

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
                  command=lambda : self.parent.switch_page(Index_page.Index_page))
        btn.grid(row=2, column=0, columnspan=2, **pad_opt)
        
        
    def register_face(self, name='Unknown', face_img_dir='face_gallery'):
        save_dir = join(face_img_dir, name)
        makedirs(save_dir, exist_ok=True)
        self.face_detector.detection(save_dir)