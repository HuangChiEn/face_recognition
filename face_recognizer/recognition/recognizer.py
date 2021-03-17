# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:19:30 2021

@author: josep
"""
import cv2
import copy
import glob
from os.path import join
from os import listdir, sep 

from keras.utils import to_categorical
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np

import inception_resnet_v1 as face_model

class Face_Recognizer:
    
    def __init__(self, pretrain_path=None):
        # pretrain weight path for face detector
        path = join("face_recognizer", "recognition")
        self.__weight_path = {"front_face":join(path, "weights", "Haar", "frontalface.xml"),
                              "profile_face":join(path, "weights", "Haar", "profileface.xml")}
        
        ## frame preprocessing :
        rgb2gray = lambda img : cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist_equ = lambda img : cv2.equalizeHist(img)
        self.__prepro_func = lambda x : hist_equ(rgb2gray(x))
        
        # face classifier
        self.model = face_model.InceptionResNetV1(input_shape=(160, 160, 3), 
                                                  weights_path=join(path, "weights", "Incept", "facenet_keras_weights.h5"))
        self.clf = SVC(kernel='linear', probability=True)
        
        
    def __signal_handler(self, sign, frame):
        self.is_interrupted = True
    
    def detection(self, save_dir=None, save_margin=10):
        
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
        
        
    def __calc_embs(self, imgs, margin, batch_size):
        def prewhiten(x):
            if x.ndim == 4:
                axis = (1, 2, 3)
                size = x[0].size
            elif x.ndim == 3:
                axis = (0, 1, 2)
                size = x.size
            else:
                raise ValueError('Dimension should be 3 or 4')
        
            mean = np.mean(x, axis=axis, keepdims=True)
            std = np.std(x, axis=axis, keepdims=True)
            std_adj = np.maximum(std, 1.0/np.sqrt(size))
            y = (x - mean) / std_adj
            return y
        
        def l2_normalize(x, axis=-1, epsilon=1e-10):
            output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
            return output
        
        def resize(img):
            return cv2.resize(img, (160, 160))
        
        aligned_images = prewhiten(imgs)
        pd = []
        for start in range(0, len(aligned_images), batch_size):
            imgs = resize(aligned_images[start:start+batch_size])
            batch_imgs = np.expand_dims(imgs, axis=0)
            embs_vec = self.model.predict(batch_imgs)
            pd.append(embs_vec.reshape(-1))  # svm fit 2-d vector
        #embs = l2_normalize(pd)
        return pd

    
    def __ld_data_gen(self):
        def data_gen(all_path):
            for path in all_path:
                img = cv2.imread(path)
                label = path.split(sep)[-2]
                yield (img, label)
            
        gal_dir = "face_gallery"
        name_dirs = listdir(gal_dir)
        all_path = []
        for name_dir in name_dirs:
            path = join(gal_dir, name_dir, "*")
            all_path.extend(glob.glob(path))
        return data_gen(all_path)

    def update_classfier(self):
        embs, labels = [], []
        gallery_data = self.__ld_data_gen()
        for idx, (img, label) in enumerate(gallery_data):
            embs_ = self.__calc_embs(img, margin=10, batch_size=1)    
            print(idx)
            labels.append(label)
            embs.append(embs_)
            
        # label processing 
        le = LabelEncoder().fit(labels)
        y = le.transform(labels)
        embs = [ e[0] for e in embs]
        
        # training phase
        clf = SVC(kernel='linear', probability=True).fit(embs, y)
        
        # update the labelencoder & classifier 
        self.le = le
        self.clf = clf
        
    
    def recognition(self):
        
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
        
        detector = detector_setting()
        vdo_src = vdo_src_setting()
        ret = True
        
        while ret:
            ret, frame = vdo_src.read()
            img = self.__prepro_func(frame)
            out_fram = copy.deepcopy(frame)
            
            bbox = detection(detector["front_detect"], img)
            if isinstance(bbox, tuple):
                bbox = detection(detector["profile_detect"], img)
            
            for (x, y, w, h) in bbox:
                cv2.rectangle(out_fram, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # output prediction result
            cv2.imshow('frame', out_fram)
            cv2.putText(out_fram, "Unknown", (x, y+10), cv2.FONT_HERSHEY_PLAIN, 
                        1, (0, 255, 255), 1, cv2.LINE_8)
                
            try:    
                crp_im = frame[y:y+h+10, x:x+w+10, :]
                embd = self.__calc_embs(crp_im, margin=10, batch_size=1)
                pred = self.le.inverse_transform(self.clf.predict(embd))
                
                # output prediction result
                cv2.imshow('frame', out_fram)
                cv2.putText(img, pred, (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 1, cv2.LINE_AA)
            except Exception as ex:
                print("Exception : {}".format(ex))
                print("cause save image error..")
                break
                
        release_src(vdo_src)
        
    
if __name__ == "__main__":
    f = Face_Recognizer()
    f.update_classfier()
    #detector.face_detection(save_dir="./tmp")
