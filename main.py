# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:10:32 2021

@ The face recognition can be build fastly due to lot of 
@ open source author.. thanks for 
@ little contributor : joseph
"""

from gui import Recognizer_GUI as gui
from gui.Pages.Index_page import Index_page

from threading import Thread

from face_recognizer.classifier.classifier import Face_Classifier
from face_recognizer.detector.detector import Face_Detector


def init_task(btn_call_bk):
    Face_Detector() ; Face_Classifier()
    btn_call_bk()
    

if __name__ == "__main__":
    
    main_win = gui.Recognizer_GUI()
    
    task = Thread(target=init_task, args=(main_win.callbk,))
    task.start()
    
    main_win.mainloop()  # Activate loop for listen event
    
    # Python will call join auto, but we should do it explicitly 
    task.join()
    
    
    