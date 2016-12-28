#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import cv2
import os


#얼굴이미지
face_dir="crop"

#모델
model_eigenface= cv2.createEigenFaceRecognizer()


imgs = []
tags = []
index = 0

for(subdir,dirs,files) in os.walk(face_dir):
    for subdir in dirs:
        img_path=os.path.join(face_dir, subdir)
        #print "img_path:", img_path
        for fn in os.listdir(img_path):
            path=img_path+"\\"+fn

            tag = index
            imgs.append(cv2.imread(path,0))
            tags.append(int(tag))
            print "path: ", path, "tag:", tag
        index += 1

(imgs, tags) = [np.array(item) for item in [imgs, tags]]

#학습
model_eigenface.train(imgs, tags)
model_eigenface.save("eigenface.xml")
print "make eigenface model is done....."

