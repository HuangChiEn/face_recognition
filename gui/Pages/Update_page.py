# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:25:34 2021

@author: josep
"""
from os.path import join
import sys

#sys.path.append(join("face_recognizer", "classifier"))
#from classifier import Face_Classifier
from face_recognizer.classifier.classifier import Face_Classifier

import tkinter as tk
from . import Index_page

class Update_page(tk.Frame):
    ## Update_page
    # update the classifier with new register
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FF6666")
        self.cls = Face_Classifier()
        self.setup_UI()

    def setup_UI(self):
        pad_opt = {'ipadx':5, 'ipady':5, 'padx':5, 'pady':5}
        
        btn = tk.Button(text="update system", master=self,
                  command=lambda : self.cls.update_classifier())
        btn.grid(row=2, column=0, columnspan=2, **pad_opt)
        
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page.Index_page)
                    ).grid(row=3, column=0, columnspan=2, **pad_opt)
        
        
        