# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:06:31 2019

@author: 37151
"""

import numpy as np
import cv2


imgname1 = 'D:\\Bishe\\markGUI\\markGUI\\picture\\001/A_001.jpg'
imgname2 = 'D:\\Bishe\\markGUI\\markGUI\\picture\\001/B_001.jpg'

surf = cv2.xfeatures2d.SIFT_create()
#sift = cv.xfeatures2d.SIFT_create()

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params,search_params)

img1 = cv2.imread(imgname1)
img1 = cv2.resize(img1,(800,600) , interpolation = cv2.INTER_AREA)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) #灰度处理图像
kp1, des1 = surf.detectAndCompute(img1,None)#des是描述子

img2 = cv2.imread(imgname2)
img2 = cv2.resize(img2,(800,600) , interpolation = cv2.INTER_AREA)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
kp2, des2 = surf.detectAndCompute(img2,None)

#hmerge = np.hstack((gray1, gray2)) #水平拼接
#cv2.imshow("gray", hmerge) #拼接显示为gray
#cv2.waitKey(0)

#img3 = cv2.drawKeypoints(img1,kp1,img1,color=(255,0,255))
#img4 = cv2.drawKeypoints(img2,kp2,img2,color=(255,0,255))

#hmerge = np.hstack((img3, img4)) #水平拼接
#cv2.imshow("point", hmerge) #拼接显示为gray
#cv2.waitKey(0)

matches = flann.knnMatch(des1,des2,k=2)

good = []
num = 0
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append([m])
        num +=1
rate = num/len(matches)
print(rate)
#img5 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
#cv2.imshow("SURF", img5)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
