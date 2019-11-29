#Canny边缘提取
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import scipy.stats



def match(img1,img2,box1):
    
    #img = cv2.cvtColor(numpy.asarray(img2),cv2.COLOR_RGB2BGR)
    #template = cv2.cvtColor(numpy.asarray(temp),cv2.COLOR_RGB2BGR)
    img = img2
    template = img1[box1[1]:box1[3],box1[0]:box1[2]]
    w, h = template.shape[::-1]

    methods = ['cv2.TM_SQDIFF']
#methods = ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED',
#            'cv2.TM_CCORR','cv2.TM_CCORR_NORMED',
#            'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED']

    for meth in methods:
        method = eval(meth)

        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) #找到最大值和最小值

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    box=top_left+bottom_right
    
    return box


def wtt(edge,row,column):
    w_edge = edge.shape[0]
    h_edge = edge.shape[1]
    a = np.empty([0,0], dtype = int)
    #a = []
    for i in range(row):
        for j in range(column):
            a = np.append(a,np.sum(edge[h_edge*i//row:h_edge*(i+1)//row,w_edge*j//column:h_edge*(j+1)//column])//255)
            #print(a)
    return a
def judge_edge(img1,img2,boxx):
    img_gray1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE) #读入灰度图像
    #img_gray_data.ravel()的ravel是把图像由二维变成1维
    img_gray2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE) #读入灰度图像
    box1 = match(img_gray1,img_gray2,boxx)
 
    img_gray11 = img_gray1[boxx[1]:boxx[3],boxx[0]:boxx[2]]
    img_gray22 = img_gray2[box1[1]:box1[3],box1[0]:box1[2]]
 
    edge1 = cv2.Canny(img_gray11,50,150)
    cv2.imshow('1',edge1)
    cv2.waitKey(0)
    edge2 = cv2.Canny(img_gray22,50,150)
    
 
    e1 = wtt(edge1,10,10)
    print(e1)
    e2 = wtt(edge2,10,10)

    # ravel1 = np.array(edge1.ravel())
    # ravel2 = np.array(edge2.ravel())
    
    # sum1 = sum(ravel1)
    # ravel1 = ravel1/sum1
    # sum2 = sum(ravel2)
    # ravel2 = ravel2/sum2
    
    # M=(ravel1+ravel2)/2
    # js = 0.5*scipy.stats.entropy(ravel1, M)+0.5*scipy.stats.entropy(ravel2, M)
    #js=  0.5*np.sum(ravel1*np.log(ravel1/M)+ravel2*np.log(ravel2/M))
    m = (e1+e2)/2
    js = 0.5*scipy.stats.entropy(e1, m)+0.5*scipy.stats.entropy(e2, m)
    print(js)
    
# img = cv2.imread('C:\\Users\\37151\\Desktop\\consistency\\aaaa\\1.jpg',cv2.COLOR_RGB2GRAY)
# edge = cv2.Canny(img,50,150)
# print(edge)
# cv2.imshow('canny',edge)
# cv2.waitKey(0)
judge_edge('C:\\Users\\37151\\Desktop\\consistency\\focus\\13.jpg','C:\\Users\\37151\\Desktop\\consistency\\focus\\4.jpg',(280,200,3800,2800))