# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:10:32 2021

@ The face recognition can be build fastly due to lot of 
@ open source author.. thanks for 
@ little contributor : joseph
"""

from gui import Recognizer_GUI as gui

#from face_recognizer.classifier.classifier import Face_Classifier
#from face_recognizer.detector.detector import Face_Detector
    
#import threading

if __name__ == "__main__":
    # multi-threading without suspend the program
    # multi-thread can not related with tkinter obj, due to tcl interpreter
    #init_task = lambda : Face_Detector() ; Face_Classifier()
    #init_thread = threading.Thread(target=init_task)
    #init_thread.start()
    
    main_win = gui.Recognizer_GUI()
    main_win.mainloop()  # Activate loop for listen event
    
    # Clear_session
    from keras import backend as K
    K.clear_session()
    