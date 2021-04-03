# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 09:58:21 2020

@author: josep
"""
from os.path import join
import sys

sys.path.append(join("face_recognizer", "detector"))
from detector import Face_Detector

sys.path.append(join("face_recognizer", "classifier"))
from classifier import Face_Classifier

sys.path.append(join("gui", "Pages"))
from Pages import Index_page

import tkinter as tk


class Recognizer_GUI(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        ## Initialize singleton 
        self.__detector_singleton_init = Face_Detector()
        self.__classifier_singleton_init = Face_Classifier()
        
        self.setup_root_cfg()
        self.__curr_page = None
        self.init_page()
    
    def setup_root_cfg(self):
        self.title("Face Recognizer")
        self.geometry("800x600")
        self.resizable(height=True, width=True)
        self.configure(background='#FFFF99')
        self.iconbitmap(join("gui", "media_src", "icon", "recog_logo.ico"))
        
    def init_page(self):
        self.switch_page(Index_page)
       
    def switch_page(self, frame_class):    
        new_page = frame_class(self)
        
        if(self.__curr_page != None):
            self.__curr_page.destroy()
            
        self.__curr_page = new_page
        self.__curr_page.pack(expand=True)
        
if __name__ == "__main__":
    pass        
