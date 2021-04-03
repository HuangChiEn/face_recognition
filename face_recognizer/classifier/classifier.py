# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:19:30 2021

@author: josep
"""
import cv2
from glob import glob
import pickle
from os.path import join
from os import listdir, sep
from itertools import chain
from random import shuffle

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np

import inception_resnet_v1 as face_model


# decorator singleton prevent __init__ twices
def singleton(clz):  
    instances = {}  
    def getinstance(*args, **kwargs):  
        if clz not in instances:  
            instances[clz] = clz(*args, **kwargs)  
  
        return instances[clz]  
  
    return getinstance  


@singleton
class Face_Classifier:
    name_dict = {"model":"facenet_keras_weights.h5", 
                 "clf":"clf.pickle", "le":"le.pickle"}
    
    def __init__(self, pretrain_path=None, ld_pick=True):
        def chk_model_weight_info():
            all_weight = listdir(join(self.base_dir, "weights"))
            return self.name_dict['model'] in all_weight
        
        self.base_dir = join("face_recognizer", "classifier")
        
        ## frame preprocessing :
        rgb2gray = lambda img : cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist_equ = lambda img : cv2.equalizeHist(img)
        self.__prepro_func = lambda x : hist_equ(rgb2gray(x))
        
        ## recognition model prepare 
        self.__ld_clf_le()
        if chk_model_weight_info():
            self.model = face_model.InceptionResNetV1(input_shape=(160, 160, 3), 
                                    weights_path=join(self.base_dir, "weights", self.name_dict['model']))
        
        
    def __calc_embs(self, imgs, margin, batch_size):
        preprocess = lambda img : np.expand_dims(cv2.resize(img, (160, 160)), axis=0)
        imgs = preprocess(imgs)
        embs_vec = self.model.predict(imgs)
        return embs_vec

    def __ld_clf_le(self):
        # check pretrain weights of 'embed model', 'classifier' and 'label encoder'
        def chk_cls_pick_info():
            all_weight = listdir(join(self.base_dir, "weights"))
            return self.name_dict['clf'] in all_weight and self.name_dict['le'] in all_weight
        
        if chk_cls_pick_info():
            clf_path = join(self.base_dir, "weights", self.name_dict['clf'])
            le_path = join(self.base_dir, "weights", self.name_dict['le'])
            with open(clf_path, 'rb') as clf_wrt, open(le_path, 'rb') as le_wrt:
                self.clf = pickle.load(clf_wrt)
                self.le = pickle.load(le_wrt)
                print("load clf & le done\n")
        
    
    def update_classifier(self, lim_num=None):
        
        def ld_data_gen():
            def data_gen(all_path):
                for path in all_path:
                    img = cv2.imread(path)
                    label = path.split(sep)[-2]
                    yield (img, label)
                
            gal_dir = "face_gallery"
            name_dirs = listdir(gal_dir)
            dirs_path = [ glob(join(gal_dir, name_dir, "*")) for name_dir in name_dirs]
            all_path = [img_path for img_path in chain.from_iterable(dirs_path)]
            shuffle(all_path)
            return data_gen(all_path), len(all_path)
        
        
        embs, labels = [], []
        gallery_data, iter_len = ld_data_gen()
        
        for idx, (img, label) in enumerate(gallery_data, 1):
            embs_ = self.__calc_embs(img, margin=10, batch_size=1)    
            labels.append(label)
            embs.append(embs_)
            print("Embedding Progress : {} / {} \n".format(idx, iter_len))    
            
        # label processing 
        le = LabelEncoder().fit(labels)
        y = le.transform(labels)
        embs = [ e[0] for e in embs]
        
        print("{}\n\n\n{}".format(labels, y))
        
        # training phase
        print("Fitting classifier.. ")
        clf = SVC(kernel='linear', probability=True).fit(embs, y)
        print("done..")
        
        # pickle the labelencoder & classifier 
        clf_path = join(self.base_dir, "weights", self.name_dict['clf'])
        le_path = join(self.base_dir, "weights", self.name_dict['le'])
        
        with open(clf_path, 'wb') as clf_wrt, open(le_path, 'wb') as le_wrt:
            pickle.dump(clf, clf_wrt)
            pickle.dump(le, le_wrt)
        # reload classifier & label encoder
        self.__ld_clf_le() 
        
        
    def recognition(self, crp_im, out_fram, text_cords):
        embd = self.__calc_embs(crp_im, margin=10, batch_size=1)
        res = self.clf.predict(embd)
        pred = self.le.inverse_transform(res)
        
        # output prediction result
        (x, y) = text_cords
        cv2.putText(out_fram, pred[0], (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 1, cv2.LINE_AA)
        
    
if __name__ == "__main__":
    f = Face_Classifier()
    pass