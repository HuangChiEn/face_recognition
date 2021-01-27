# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:45:26 2021

"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import signal
from IPython import display

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from skimage.transform import resize
from keras.models import load_model

from os import join

class FaceDemo(object):
    def __init__(self, cascade_path):
        self.vc = None
        self.margin = 10
        self.batch_size = 1
        self.n_img_per_person = 10
        self.data = {}
        self.le = None
        self.clf = None
             
    def calc_embs(self, imgs, margin, batch_size):
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
        
        aligned_images = prewhiten(imgs)
        pd = []
        for start in range(0, len(aligned_images), batch_size):
            pd.append(self.model.predict_on_batch(aligned_images[start:start+batch_size]))
        embs = l2_normalize(np.concatenate(pd))
    
        return embs
                   
    
    def train(self):
        labels = []
        embs = []
        for name, imgs in self.data.items():
            embs_ = self.calc_embs(imgs, self.margin, self.batch_size)    
            labels.extend([name] * len(embs_))
            embs.append(embs_)

        embs = np.concatenate(embs)
        le = LabelEncoder().fit(labels)
        y = le.transform(labels)
        clf = SVC(kernel='linear', probability=True).fit(embs, y)
        
        self.le = le
        self.clf = clf
        
    def infer(self):
        vc = cv2.VideoCapture(0)
        self.vc = vc
        if vc.isOpened():
            is_capturing, _ = vc.read()
        else:
            is_capturing = False

        signal.signal(signal.SIGINT, self._signal_handler)
        self.is_interrupted = False
        while is_capturing:
            is_capturing, frame = vc.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.cascade.detectMultiScale(frame,
                                         scaleFactor=1.1,
                                         minNeighbors=3,
                                         minSize=(100, 100))
            pred = None
            if len(faces) != 0:
                face = faces[0]
                (x, y, w, h) = face
                left = x - self.margin // 2
                right = x + w + self.margin // 2
                bottom = y - self.margin // 2
                top = y + h + self.margin // 2
                img = resize(frame[bottom:top, left:right, :],
                             (160, 160), mode='reflect')
                embs = self.calc_embs(img[np.newaxis], self.margin, 1)
                pred = self.le.inverse_transform(self.clf.predict(embs))
                cv2.rectangle(frame,
                              (left-1, bottom-1),
                              (right+1, top+1),
                              (255, 0, 0), thickness=2)
            plt.imshow(frame)
            plt.title(pred)
            plt.xticks([])
            plt.yticks([])
            display.clear_output(wait=True)
            try:
                plt.pause(0.1)
            except Exception:
                pass
            if self.is_interrupted:
                vc.release()
                break


