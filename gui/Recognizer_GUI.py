# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 09:58:21 2020

@author: josep
"""
from os.path import join
import sys

from .Pages import Index_page, Loading_page
import tkinter as tk

from face_recognizer.classifier.classifier import Face_Classifier
from face_recognizer.detector.detector import Face_Detector

class Recognizer_GUI(tk.Tk):
    
    def __init__(self):
        
        def setup_root_cfg():
            self.title("Face Recognizer")
            self.geometry("800x600")
            self.resizable(height=True, width=True)
            self.configure(background='#FFFF99')
            self.iconbitmap(join("gui", "media_src", "icon", "recog_logo.ico"))
        
        tk.Tk.__init__(self)
        
        setup_root_cfg()
        self.__curr_page = None
        
        # initial Index page
        self.switch_page(Index_page.Index_page, init_flg=True)
        
       
    def switch_page(self, frame_class, init_flg=False):    
        new_page = frame_class(self)
        
        if(self.__curr_page != None):
            self.__curr_page.destroy()
            
        self.__curr_page = new_page
        self.__curr_page.pack(expand=True)
        
        # HACKME : bad implementation..
        if isinstance(self.__curr_page, Index_page.Index_page): 
            self.callbk = self.__curr_page.switch_state
            init_flg == False and self.__curr_page.switch_state()
        
        
if __name__ == "__main__":
    pass        
