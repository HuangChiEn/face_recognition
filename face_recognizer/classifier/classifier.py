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

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np

from tensorflow.keras.models import model_from_json
import inception_resnet_v1 as face_model


class Face_Classifier:
    name_dict = {"model":"facenet_keras_weights.json", "clf":"clf.pickle",
                   "le":"le.pickle"}
    
    def __init__(self, pretrain_path=None, ld_pick=True):
        # check pretrain weights of 'embed model', 'classifier' and 'label encoder'
        def chk_cls_pick_info():
            all_weight = listdir(join(self.base_dir, "weights"))
            return self.name_dict['clf'] in all_weight and self.name_dict['le'] in all_weight
        def chk_model_weight_info():
            all_weight = listdir(join(self.base_dir, "weights"))
            return self.name_dict['model'] in all_weight
            
        ## frame preprocessing :
        rgb2gray = lambda img : cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist_equ = lambda img : cv2.equalizeHist(img)
        self.__prepro_func = lambda x : hist_equ(rgb2gray(x))
        
        self.base_dir = join("face_recognizer", "classifier")
        
        if chk_model_weight_info():
            js_path = join(self.base_dir, "weights", self.name_dict['model'])
            with open(js_path, "rb") as f_ptr:
                    self.model = model_from_json(f_ptr.read())
        else:   
            self.model = face_model.InceptionResNetV1(input_shape=(160, 160, 3), 
                                    weights_path=join(self.base_dir, "weights", self.name_dict['model']))
      
        if chk_cls_pick_info():
            clf_path = join(self.base_dir, "weights", self.name_dict['clf'])
            le_path = join(self.base_dir, "weights", self.name_dict['le'])
            with open(clf_path, 'rb') as clf_wrt, open(le_path, 'rb') as le_wrt:
                self.clf = pickle.load(clf_wrt)
                self.le = pickle.load(le_wrt)
        else:
            self.clf = SVC(kernel='linear', probability=True)
        
        
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
        im = np.expand_dims(resize(aligned_images), axis=0)
        embs_vec = self.model.predict(im)
        return embs_vec  # l2_norm
    
    def __ld_data_gen(self):
        
        def data_gen(all_path):
            for path in all_path:
                img = cv2.imread(path)
                label = path.split(sep)[-2]
                yield (img, label)
            
        gal_dir = "face_gallery"
        name_dirs = listdir(gal_dir)
        dirs_path = [ glob(join(gal_dir, name_dir, "*")) for name_dir in name_dirs]
        all_path = [img_path for img_path in chain.from_iterable(dirs_path)]
        
        return data_gen(all_path), len(all_path)
    

    def update_classfier(self, lim_num=None):
        embs, labels = [], []
        gallery_data, iter_len = self.__ld_data_gen()
        
        for idx, (img, label) in enumerate(gallery_data):
            embs_ = self.__calc_embs(img, margin=10, batch_size=1)    
            labels.append(label)
            embs.append(embs_)
            print("Progress : {} / {} \n".format(idx, iter_len+1))    
            
        # label processing 
        le = LabelEncoder().fit(labels)
        y = le.transform(labels)
        embs = [ e[0] for e in embs]
        
        # training phase
        clf = SVC(kernel='linear', probability=True).fit(embs, y)
        
        # pickle the labelencoder & classifier 
        clf_path = join(self.base_dir, "weights", self.name_dict['clf'])
        le_path = join(self.base_dir, "weights", self.name_dict['le'])
        with open(clf_path, 'wb') as clf_wrt, open(le_path, 'wb') as le_wrt:
            pickle.dump(clf, clf_wrt)
            pickle.dump(le, le_wrt)
        
        
    def recognition(self, crp_im, out_fram, text_cords):
        embd = self.__calc_embs(crp_im, margin=10, batch_size=1)
        pred = self.le.inverse_transform(self.clf.predict(embd))
        
        # output prediction result
        (x, y) = text_cords
        cv2.putText(out_fram, pred[0], (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 1, cv2.LINE_AA)
        
    
if __name__ == "__main__":
    f = Face_Classifier()
    