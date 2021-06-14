# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:11:34 2021

@author: josep
"""
from os.path import join
import sys

from face_recognizer.detector.detector import Face_Detector
from face_recognizer.classifier.classifier import Face_Classifier

import tkinter as tk
from . import Index_page

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
                  command=lambda : self.parent.switch_page(Index_page.Index_page))
        recg_btn.grid(row=1, column=0)
        
    def face_recognition(self):
        self.detector.recog_detect(self.classifier)

