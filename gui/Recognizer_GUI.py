# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 09:58:21 2020

@author: josep
"""
from os.path import join
import sys
sys.path.append(join("gui", "Pages"))
from Pages import Index_page


class Recognizer_GUI(object):
    def __init__(self, parent, **kwargs):
        self.root = parent
        self.setup_root_cfg()
        self.__curr_page = None
        self.init_page()
    
    def setup_root_cfg(self):
        self.root.title("Face Recognizer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(background='#FFFF99')
        self.root.iconbitmap(join("gui", "media_src", "icon", "recog_logo.ico"))
        
    def init_page(self):
        self.switch_page(Index_page)
       
    def switch_page(self, frame_class):    
        new_page = frame_class(self.root)
        if(self.__curr_page != None):
            self.__curr_page.destroy()
        self.__curr_page = new_page
        self.__curr_page.pack(expand=1)
        
if __name__ == "__main__":
    pass
    #main_win = tk.Tk()
    #Recognizer_GUI(main_win)
    
    # Activate loop for listen event
    #main_win.mainloop()           
