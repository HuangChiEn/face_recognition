# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:19:30 2021

@author: josep
"""
import cv2
from os.path import join
import copy
#import signal

class Face_Detector:
    
    def __init__(self, pretrain_path=None):
        # pretrain weight path for face detector
        path = join("face_recognizer", "detector")
        self.__weight_path = {"front_face":join(path, "weights", "Haar", "frontalface.xml"),
                              "profile_face":join(path, "weights", "Haar", "profileface.xml")}
            
        ## frame preprocessing :
        rgb2gray = lambda img : cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist_equ = lambda img : cv2.equalizeHist(img)
        self.__prepro_func = lambda x : hist_equ(rgb2gray(x))
        
        
    def __signal_handler(self, sign, frame):
        self.is_interrupted = True
    
    def face_detection(self, save_dir=None, save_margin=10):
        
        def vdo_src_setting():
            web_cam = cv2.VideoCapture(0)
            (web_cam.isOpened() == False) and web_cam.open(0)
            return web_cam
        
        def detector_setting():
            model_type = lambda typ : cv2.CascadeClassifier(self.__weight_path[typ])
            return {'front_detect':model_type('front_face'), 
                    'profile_detect':model_type("profile_face")}
            
        def detection(faceCascade, img):
            bbox = faceCascade.detectMultiScale(
                    img,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(35, 35),
                    flags = cv2.CASCADE_DO_CANNY_PRUNING #cv2.CASCADE_SCALE_IMAGE 
                )
            return bbox
        
        def release_src(vdo_src):
            vdo_src.release()
            cv2.destroyAllWindows()
        
        #signal.signal(signal.SIGINT, self._signal_handler)
        #self.is_interrupted = False
        detector = detector_setting()
        vdo_src = vdo_src_setting()
        ret = True
        cnt = 0
        
        while ret:
            ret, frame = vdo_src.read()
            img = self.__prepro_func(frame)
            out_fram = copy.deepcopy(frame)
            
            bbox = detection(detector["front_detect"], img)
            if isinstance(bbox, tuple):
                bbox = detection(detector["profile_detect"], img)
            
            for (x, y, w, h) in bbox:
                cv2.rectangle(out_fram, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            cv2.imshow('frame', out_fram)
            
            try:
                in_key = cv2.waitKey(1) & 0xFF
                if in_key == ord(" "):
                    crp_im = frame[y:y+h+save_margin, x:x+w+save_margin, :]
                    cv2.imwrite(join(save_dir, "{}.jpg").format(cnt), crp_im)
                    cnt = cnt + 1
                elif in_key == ord("q"): 
                    break
            except Exception as ex:
                print("Exception : {}".format(ex))
                print("cause save image error..")
                break
                
        release_src(vdo_src)

if __name__ == "__main__":
    pass
    #detector = Face_Detector()
    #detector.face_detection(save_dir="./tmp")
