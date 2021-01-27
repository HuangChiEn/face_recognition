# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:10:32 2021

@ The face recognition can be build fastly due to lot of 
@ open source author.. thanks for 
@ little contributor : josep
"""

from gui import Recognizer_GUI as gui_wrap
import tkinter as tk

if __name__ == "__main__":
    main_win = tk.Tk()
    gui_wrap.Recognizer_GUI(main_win)
    
    # Activate loop for listen event
    main_win.mainloop()
