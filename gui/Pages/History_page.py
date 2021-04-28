# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:11:35 2021

@author: josep
"""
import tkinter as tk
from . import Index_page

class History_page(tk.Frame):
    ## History page : 
    # 1. review the login record of the recognition system
    # 2. markdown the invalid login which show the input image
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, background="#FFFFCC")
        self.setup_UI()
        
    def setup_UI(self):
        tk.Button(self, text="back to menu", command=lambda: self.parent.switch_page(Index_page.Index_page)
                    ).grid(row=0)