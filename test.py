#coding=utf-8
import cv2
from PIL import Image, ImageTk
import numpy as np
import tkinter.filedialog
import tkinter as tk 
import os
#import threading
#import time
from tkinter import ttk
import json
import csv


import tkinter.messagebox 

window = tk.Tk()   #创建根窗口
 
top = tk.Toplevel(window)   #创建顶层窗口，用于在双击时弹窗显示点击的图片
top.destroy()   #顶层窗口暂时不用，双击时才会弹出
marktop = tk.Toplevel(window)   #创建顶层窗口，用于在双击时弹窗显示点击的图片
cmb = ttk.Combobox(marktop)
cmb2 = ttk.Combobox(marktop)
marktop.destroy()   #顶层窗口暂时不用，双击时才会弹出
var1 = tk.DoubleVar() 
var2 = tk.DoubleVar() 
var3 = tk.DoubleVar() 
var4 = tk.DoubleVar() 

group = 1

#该函数通过文件夹的路径path可以生成一个数组，数组的元素均为文件夹下每一张图片的绝对路径
def getfilesname(path):
    filesname =[]
    if(path != '' and path != ()):
        dirs = os.listdir(path)
        for i in dirs:
            if os.path.splitext(i)[1] == ".jpg" or os.path.splitext(i)[1] == ".png" or os.path.splitext(i)[1] == ".JPG" or os.path.splitext(i)[1] == ".jpeg" :
                filesname+=[path+'/'+i]
    else:
        filesname = []
    return filesname

#该函数用于切换文件夹，当“选择路径”按钮按下时出发
#该函数包含众多全局变量，并对其一一修改
def selectPath():
    global pathh
    global path
    global group
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale,w_img,h_img,w_win,h_win
    global senseid,phoneidstart
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4  #用于双击弹出图片
    global data
    global flag
    global rect_box
    Labins.destroy()
    group = 1
    
    rect_box = [0,0,0,0]
    if(data != []):
        save()
    path = tkinter.filedialog.askdirectory() 
    filesname = getfilesname(path)

    #判断文件夹是否合法
    # while(len(filesname) == 0 or len(filesname)%4 != 0):
    while(len(filesname) == 0):
        path = tkinter.filedialog.askdirectory()
        filesname = getfilesname(path)
    pathh.set(path)
    filesname = getfilesname(path)
    print(filesname)
    senseid = path.split('/')[-1]
    phoneidstart = 1
    sum = len(filesname)
    string = 'sum:'+str(sum)+';group:'+str(group)
    tk.Label(window ,text=string).place(x=0.61*w_win, y=0.025*h_win, anchor='w')
    # #用于match算法
    # img1 = cv2.imread(filesname[0],0)
    # img2 = cv2.imread(filesname[1],0)
    # img3 = cv2.imread(filesname[2],0)
    # img4 = cv2.imread(filesname[3],0)
    
    # img_open1 = Image.open(filesname[0])
    # #print(img_open1)
    # img_open2 = Image.open(filesname[1])
    # img_open3 = Image.open(filesname[2])
    # img_open4 = Image.open(filesname[3])
    img1 = cv2.imread(filesname[(phoneidstart-1)%sum],0)
    img2 = cv2.imread(filesname[phoneidstart%sum],0)
    img3 = cv2.imread(filesname[(phoneidstart+1)%sum],0)
    img4 = cv2.imread(filesname[(phoneidstart+2)%sum],0)
    
    img_open1 = Image.open(filesname[(phoneidstart-1)%sum])
    img_open2 = Image.open(filesname[phoneidstart%sum])
    img_open3 = Image.open(filesname[(phoneidstart+1)%sum])
    img_open4 = Image.open(filesname[(phoneidstart+2)%sum])

    # img1 = cv2.cvtColor(np.asarray(img_open1), cv2.COLOR_RGB2BGR)
    # img2 = cv2.cvtColor(np.asarray(img_open2), cv2.COLOR_RGB2BGR)
    # img3 = cv2.cvtColor(np.asarray(img_open3), cv2.COLOR_RGB2BGR)
    # img4 = cv2.cvtColor(np.asarray(img_open4), cv2.COLOR_RGB2BGR)
    #print(img1.shape[1])

    # if (img1.shape[0]>img1.shape[1]):
    #     img_open1 = img_open1.rotate(270,expand = True)
    #     img_open2 = img_open2.rotate(270,expand = True)
    #     img_open3 = img_open3.rotate(270,expand = True)
    #     img_open4 = img_open4.rotate(270,expand = True)
    #https://blog.csdn.net/mizhenpeng/article/details/82794112

    w_img = img1.shape[1]
    h_img = img1.shape[0]
    for i in range(len(filesname)):
        img = cv2.imread(filesname[i],0)
        w_img = min(w_img,img.shape[1])
        h_img = min(h_img,img.shape[0])
    # w_img = 3648
    # h_img = 2736
    #用于双击弹出图片
    if(w_img/h_img < w_win/h_win):
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.9*h_win*w_img/h_img),int(0.9*h_win))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open2.resize((int(0.9*h_win*w_img/h_img),int(0.9*h_win))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open3.resize((int(0.9*h_win*w_img/h_img),int(0.9*h_win))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open4.resize((int(0.9*h_win*w_img/h_img),int(0.9*h_win))))
    else:
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.9*w_win),int(0.9*w_win*h_img/w_img))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open1.resize((int(0.9*w_win),int(0.9*w_win*h_img/w_img))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open1.resize((int(0.9*w_win),int(0.9*w_win*h_img/w_img))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open1.resize((int(0.9*w_win),int(0.9*w_win*h_img/w_img))))

    maxscale = min(int(w_img/w_canvas),int(h_img/h_canvas))

    scale = maxscale
    
    # box 初始化操作
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box
    image_file1 = create(img_open1,box)
    image_file2 = create(img_open2,box2)
    image_file3 = create(img_open3,box3)
    image_file4 = create(img_open4,box4)

    putimage()

    if(flag==1):
        changemode()

#测试函数，无用
# def print_selection():
#     print('you have selected ' + var.get())

#原始图片通过Image.open加载，之后通过次函数，可以生成用于展示的imagefile
#注意，该函数包含全局变量，包含resize操作，慎用！！！
def create(img_open,box):
    global w_canvas,h_canvas
    region = img_open.crop(box)     

    region1 = region.resize((w_canvas, h_canvas))

    image_file = ImageTk.PhotoImage(image = region1)
    return image_file

#重要函数，用于在画布上展示图片
#image1-image4均为画布上图片的id，基本思路是：应用canvas的delete方法删除原来的展示图片，然后再换一张新的图片上去
#不要重复叠图片，会增加资源消耗
def putimage():
    #global canvas1,canvas2,canvas3,canvas4

    global box
    global w_canvas,h_canvas,maxscale
    #global image1,image2,image3,image4
    # global rect_box
    #print(canvas1.find_all())
    # rect_box = [0,0,0,0]
    canvas1.delete(canvas1.find_all())
    canvas2.delete(canvas2.find_all())
    canvas3.delete(canvas3.find_all())
    canvas4.delete(canvas4.find_all())


    image1 = canvas1.create_image(w_canvas, h_canvas, anchor='se',image=image_file1)  

    image2 = canvas2.create_image(0, h_canvas, anchor='sw',image=image_file2)     

    image3 = canvas3.create_image(w_canvas, 0, anchor='ne',image=image_file3)     

    image4 = canvas4.create_image(0, 0, anchor='nw',image=image_file4)  

def kpc(event):#event形参来获取对应事件描述
    global ctrlflag
    ctrlflag = 1#keysym显示特殊按键
  
def krc(event):#event形参来获取对应事件描述
    global ctrlflag
    ctrlflag = 0#keysym显示特殊按键  



#用于实现拖动功能
#只有在canvas上拖动才有意义（对应第一个if语句）
# 设计思路：左键按下，开始拖动，进入函数，然后不停的将鼠标当前位置（event.x，event.y）记录到全局变量loc中
# 进而判断拖动方向，修改box，实现拖动
# 新增 框选功能，用于精确打分    
def drag(event):
    global box,box2,box3,box4
    global img1,img2,img3,img4
    global image_file1,image_file2,image_file3,image_file4
    global rect1,rect2,rect3,rect4
    global loc
    global scale
    global w_canvas,h_canvas,maxscale
    global flag,ctrlflag
    global rect_box

    
    if(pathh.get() != ''):
        tmp = 0
        if (flag == 0):
            nowloc=[]
            if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):
                
                nowloc.append(event.x)
                nowloc.append(event.y)
                loc.append(nowloc)
                nowloc=[]
                if (len(loc) >= 3):
                    del loc[0]
                boxx = list(box)
                boxx2 = list(box2)
                boxx3 = list(box3)
                boxx4 = list(box4)
                boxxlist = []
                boxxlist.append(boxx)
                boxxlist.append(boxx2)
                boxxlist.append(boxx3)
                boxxlist.append(boxx4)
                if (len(loc) == 2):
                    if(ctrlflag == 0):
                        for i in range(4):
                            if boxxlist[i][0]+(loc[0][0]-loc[1][0])*scale<=0:
                                boxxlist[i][0] = 0
                            elif boxxlist[i][0]+(loc[0][0]-loc[1][0])*scale>= w_img-w_canvas*scale:
                                boxxlist[i][0] = w_img-w_canvas*scale
                            else:
                                boxxlist[i][0] = boxxlist[i][0]+(loc[0][0]-loc[1][0])*scale

                            if boxxlist[i][1]+(loc[0][1]-loc[1][1])*scale <= 0:
                                boxxlist[i][1] = 0
                            elif boxxlist[i][1]+(loc[0][1]-loc[1][1])*scale>= h_img-h_canvas*scale:
                                boxxlist[i][1]= h_img-h_canvas*scale
                            else:
                                boxxlist[i][1] = boxxlist[i][1]+(loc[0][1]-loc[1][1])*scale
                            boxxlist[i][2] = boxxlist[i][0] +w_canvas*scale
                            boxxlist[i][3] = boxxlist[i][1] +h_canvas*scale
                    else:
                        if(event.widget == canvas1):
                            tmp = 0
                        if(event.widget == canvas2):
                            tmp = 1
                        if(event.widget == canvas3):
                            tmp = 2
                        if(event.widget == canvas4):
                            tmp = 3

                        if boxxlist[tmp][0]+(loc[0][0]-loc[1][0])*scale<=0:
                            boxxlist[tmp][0] = 0
                        elif boxxlist[tmp][0]+(loc[0][0]-loc[1][0])*scale>= w_img-w_canvas*scale:
                            boxxlist[tmp][0] = w_img-w_canvas*scale
                        else:
                            boxxlist[tmp][0] = boxxlist[tmp][0]+(loc[0][0]-loc[1][0])*scale

                        if boxxlist[tmp][1]+(loc[0][1]-loc[1][1])*scale <= 0:
                            boxxlist[tmp][1] = 0
                        elif boxxlist[tmp][1]+(loc[0][1]-loc[1][1])*scale>= h_img-h_canvas*scale:
                            boxxlist[tmp][1]= h_img-h_canvas*scale
                        else:
                            boxxlist[tmp][1] = boxxlist[tmp][1]+(loc[0][1]-loc[1][1])*scale
                        boxxlist[tmp][2] = boxxlist[tmp][0] +w_canvas*scale
                        boxxlist[tmp][3] = boxxlist[tmp][1] +h_canvas*scale                    
                    
                    box = tuple(boxxlist[0])
                    box2 = tuple(boxxlist[1])
                    box3 = tuple(boxxlist[2])
                    box4 = tuple(boxxlist[3])

                
                    # box2 = box
                    # box3 = box
                    # box4 = box
                    # if (abs(time.perf_counter()-timer) >10):

                    #     box2 = match(img1,img2,box)
                    #     box3 = match(img1,img3,box)
                    #     box4 = match(img1,img4,box)
                    #     timer = time.perf_counter()  

                    image_file1 = create(img_open1,box)
                    image_file2 = create(img_open2,box2)
                    image_file3 = create(img_open3,box3)
                    image_file4 = create(img_open4,box4)

                    putimage()
        else:
            if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):
                rect_box = []
                nowloc=[]
                nowloc.append(event.x)
                nowloc.append(event.y)
                loc.append(nowloc)
                nowloc=[]
                if (len(loc) >= 3):
                    del loc[1]
                if(len(loc) == 2):
                    #print(canvas1.find_withtag('rtag'))
                    canvas1.delete(canvas1.find_withtag('rtag'))
                    canvas2.delete(canvas2.find_withtag('rtag'))
                    canvas3.delete(canvas3.find_withtag('rtag'))
                    canvas4.delete(canvas4.find_withtag('rtag'))

                    rect1 = canvas1.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3,tags=('rtag'))
                    rect2 = canvas2.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3,tags=('rtag'))
                    rect3 = canvas3.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3,tags=('rtag'))
                    rect4 = canvas4.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3,tags=('rtag'))

                    rect_box.append(loc[0][0])
                    rect_box.append(loc[0][1])
                    rect_box.append(loc[1][0])
                    rect_box.append(loc[1][1])

#用于实现滚轮控制缩放
#通过滚轮滚动事件触发函数
#滚动，修改全局变量 scale，scale进而对box作出修改
def scaler(event):
    global scale
    global box,box2,box3,box4
    global img1,img2,img3,img4
    global image_file1,image_file2,image_file3,image_file4
    global w_canvas,h_canvas,maxscale,w_win,h_win
    global flag
    # print(event.x_root,event.y_root,event.widget,event.type)
    # print(event.widget == canvas1)
    if(pathh.get() != ''):
        if(flag==0):
            if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):
    
                boxx = list(box)
                boxx2 = list(box2)
                boxx3 = list(box3)
                boxx4 = list(box4)
                boxxlist = []
                boxxlist.append(boxx)
                boxxlist.append(boxx2)
                boxxlist.append(boxx3)
                boxxlist.append(boxx4)

                oldscale = scale
                for i in range(4):
                    if((event.delta > 0 or event.num == 4) and oldscale >1):
                        scale = max(oldscale-1,1)
                        boxxlist[i][0] = boxxlist[i][0] + event.x
                        boxxlist[i][1] = boxxlist[i][1] + event.y
                
                    if((event.delta < 0 or event.num == 5) and oldscale < maxscale):
                        scale = min(oldscale+1,maxscale)
                        if (boxxlist[i][0] - event.x <0):
                            boxxlist[i][0]=0
                        elif(boxxlist[i][0] - event.x > w_img-w_canvas*scale):
                            boxxlist[i][0]=w_img-w_canvas*scale
                        else:
                            boxxlist[i][0] = boxxlist[i][0] - event.x
                        
                        if (boxxlist[i][1] - event.y <0):
                            boxxlist[i][1]=0
                        elif(boxxlist[i][1] - event.y > h_img-h_canvas*scale):
                            boxxlist[i][1]=h_img-h_canvas*scale
                        else:
                            boxxlist[i][1] = boxxlist[i][1] - event.y


                    boxxlist[i][2] = boxxlist[i][0]+w_canvas*scale
                    boxxlist[i][3] = boxxlist[i][1]+h_canvas*scale


                box = tuple(boxxlist[0])
                box2 = tuple(boxxlist[1])
                box3 = tuple(boxxlist[2])
                box4 = tuple(boxxlist[3])       
                # box = tuple(boxx)
                # box2 = box
                # box3 = box
                # box4 = box
                # box2 = match(img1,img2,box)
                # box3 = match(img1,img3,box)
                # box4 = match(img1,img4,box)

                image_file1 = create(img_open1,box)
                image_file2 = create(img_open2,box2)
                image_file3 = create(img_open3,box3)
                image_file4 = create(img_open4,box4)

                putimage()

#鼠标按键释放触发该函数，清空全局loc
#用于实现拖动
def locclear(event):
    global loc
    loc.clear()

#opencv内置算子实现在img2中找出和img相似的区域

def judge_gray():
    global img1,img2,img3,img4
    img_gray1 = img1 #读入灰度图像
    img_gray2 = img2 #读入灰度图像
    img_gray3 = img3 #读入灰度图像
    img_gray4 = img4 #读入灰度图像
    bo = (280,200,3800,2800)
    bo2 = match(img_gray1,img_gray2,bo) 
    bo3 = match(img_gray1,img_gray3,bo)
    bo4 = match(img_gray1,img_gray4,bo)
    print(bo4)
    img_gray11 = img_gray1[bo[1]:bo[3],bo[0]:bo[2]]
    img_gray22 = img_gray2[bo2[1]:bo2[3],bo2[0]:bo2[2]]
    img_gray33 = img_gray3[bo3[1]:bo3[3],bo3[0]:bo3[2]]
    img_gray44 = img_gray4[bo4[1]:bo4[3],bo4[0]:bo4[2]]
    hist1, bins1 = np.histogram(img_gray11.ravel(), bins=255)#通过histogram就可以得到每段像素值范围bins的像素点个数hist
    #img_gray_data.ravel()的ravel是把图像由二维变成1维
    hist2, bins2 = np.histogram(img_gray22.ravel(), bins=255)#通过histogram就可以得到每段像素值范围bins的像素点个数hist
    hist3, bins3 = np.histogram(img_gray33.ravel(), bins=255)#通过histogram就可以得到每段像素值范围bins的像素点个数hist
    #img_gray_data.ravel()的ravel是把图像由二维变成1维
    hist4, bins4 = np.histogram(img_gray44.ravel(), bins=255)#通过histogram就可以得到每段像素值范围bins的像素点个数hist
    vector1=np.array(hist1)
    vector2=np.array(hist2)
    vector3=np.array(hist3)
    vector4=np.array(hist4)
    distance1=np.sqrt(np.sum(np.square(vector1-vector2)))/255
    distance2=np.sqrt(np.sum(np.square(vector1-vector3)))/255
    distance3=np.sqrt(np.sum(np.square(vector1-vector4)))/255
    print(distance1)
    print(distance2)
    print(distance3)


def match(img1,img2,box1):
    img = img2
    template = img1[box1[1]:box1[3],box1[0]:box1[2]]
    w, h = template.shape[::-1]

    methods = ['cv2.TM_SQDIFF_NORMED']
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

#Ctrl+m 触发该函数
#实现图片对齐，其中调用三次match函数
#按钮 match 触发该函数
#实现图片对齐，其中调用三次match函数
def update():
    global box,box2,box3,box4
    global img1,img2,img3,img4,flag
    global image_file1,image_file2,image_file3,image_file4
    if(pathh.get() != ''):
        box2 = match(img1,img2,box)
        box3 = match(img1,img3,box)
        box4 = match(img1,img4,box)

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()

# def update_rgb():
#     global box,box2,box3,box4
#     global img1,img2,img3,img4,flag
#     global image_file1,image_file2,image_file3,image_file4

#     box2 = match_rgb(img1,img2,box)
#     box3 = match_rgb(img1,img3,box)
#     box4 = match_rgb(img1,img4,box)

#     image_file1 = create(img_open1,box)
#     image_file2 = create(img_open2,box2)
#     image_file3 = create(img_open3,box3)
#     image_file4 = create(img_open4,box4)

#     putimage()
def update_key(event):
    global box,box2,box3,box4
    global img1,img2,img3,img4,flag
    global image_file1,image_file2,image_file3,image_file4
    if(pathh.get() != ''):
        box2 = match(img1,img2,box)
        box3 = match(img1,img3,box)
        box4 = match(img1,img4,box)

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()


#该函数用于在当前文件夹下切换到接下来的四张图片
#和切换文件夹有点相似，需要改很多全局变量
def next():
    global phoneidstart
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale
    global phoneidstart
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    global rect_box
    global group
    if(pathh.get() != ''):

        group +=1
        sum = len(filesname)
        maxgroup = int(float(sum)/4+0.5)
        if(group>maxgroup):
            group = 1
        string = 'sum:'+str(sum)+';group:'+str(group)
        tk.Label(window ,text=string).place(x=0.61*w_win, y=0.025*h_win, anchor='w')
        rect_box = [0,0,0,0]
        scale =maxscale
        box = (0, 0, w_canvas*scale, h_canvas*scale)    
        box2 = box
        box3 = box
        box4 = box

        # phoneidstart = (phoneidstart+4)%sum
        # if(phoneidstart == 0):
        #     phoneidstart = sum
        phoneidstart +=4 
        if(phoneidstart>sum):
            phoneidstart = 1
        #if (phoneidstart <= len(filesname)):
        img1 = cv2.imread(filesname[(phoneidstart-1)%sum],0)
        img2 = cv2.imread(filesname[phoneidstart%sum],0)
        img3 = cv2.imread(filesname[(phoneidstart+1)%sum],0)
        img4 = cv2.imread(filesname[(phoneidstart+2)%sum],0)
        
        img_open1 = Image.open(filesname[(phoneidstart-1)%sum])
        img_open2 = Image.open(filesname[phoneidstart%sum])
        img_open3 = Image.open(filesname[(phoneidstart+1)%sum])
        img_open4 = Image.open(filesname[(phoneidstart+2)%sum])

        # if (img1.shape[0]>img1.shape[1]):
        #     img_open1 = img_open1.rotate(270,expand = True)
        #     img_open2 = img_open2.rotate(270,expand = True)
        #     img_open3 = img_open3.rotate(270,expand = True)
        #     img_open4 = img_open4.rotate(270,expand = True)
        #用于双击弹窗
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open2.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open3.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open4.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()
        #else:
            # phoneidstart -= 4
            # a = tkinter.messagebox.showwarning(message='此文件夹已结束') 
        if(flag==1):
            changemode() 
def next_key(event):
    global phoneidstart
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale
    global phoneidstart
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    global rect_box
    global group
    if(pathh.get() != ''):
        group +=1
        sum = len(filesname)
        maxgroup = int(float(sum)/4+0.5)
        if(group>maxgroup):
            group = 1
        string = 'sum:'+str(sum)+';group:'+str(group)
        tk.Label(window ,text=string).place(x=0.61*w_win, y=0.025*h_win, anchor='w')
        rect_box = [0,0,0,0]
        scale =maxscale
        box = (0, 0, w_canvas*scale, h_canvas*scale)    
        box2 = box
        box3 = box
        box4 = box

        # phoneidstart = (phoneidstart+4)%sum
        # if(phoneidstart == 0):
        #     phoneidstart = sum
        phoneidstart +=4 
        if(phoneidstart>sum):
            phoneidstart = 1
        #if (phoneidstart <= len(filesname)):
        img1 = cv2.imread(filesname[(phoneidstart-1)%sum],0)
        img2 = cv2.imread(filesname[phoneidstart%sum],0)
        img3 = cv2.imread(filesname[(phoneidstart+1)%sum],0)
        img4 = cv2.imread(filesname[(phoneidstart+2)%sum],0)
        
        img_open1 = Image.open(filesname[(phoneidstart-1)%sum])
        img_open2 = Image.open(filesname[phoneidstart%sum])
        img_open3 = Image.open(filesname[(phoneidstart+1)%sum])
        img_open4 = Image.open(filesname[(phoneidstart+2)%sum])

        # if (img1.shape[0]>img1.shape[1]):
        #     img_open1 = img_open1.rotate(270,expand = True)
        #     img_open2 = img_open2.rotate(270,expand = True)
        #     img_open3 = img_open3.rotate(270,expand = True)
        #     img_open4 = img_open4.rotate(270,expand = True)
        #用于双击弹窗
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open2.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open3.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open4.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()
        #else:
            # phoneidstart -= 4
            # a = tkinter.messagebox.showwarning(message='此文件夹已结束') 
        if(flag==1):
            changemode() 


def previous():
    global phoneidstart
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale
    global phoneidstart
    global flag
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    global rect_box
    global group
    if(pathh.get() != ''):
        group -= 1
        sum = len(filesname)
        maxgroup = int(float(sum)/4+0.5)
        if(group<1):
            group = maxgroup
        string = 'sum:'+str(sum)+';group:'+str(group)
        tk.Label(window ,text=string).place(x=0.61*w_win, y=0.025*h_win, anchor='w')
        rect_box = [0,0,0,0]
        scale =maxscale
        box = (0, 0, w_canvas*scale, h_canvas*scale)    
        box2 = box
        box3 = box
        box4 = box

        # phoneidstart = (phoneidstart-4+sum)%sum
        # if(phoneidstart == 0):
        #     phoneidstart = sum
        phoneidstart -=4 
        if(phoneidstart <1):
            phoneidstart = (maxgroup-1)*4+1

        img1 = cv2.imread(filesname[(phoneidstart-1)%sum],0)
        img2 = cv2.imread(filesname[phoneidstart%sum],0)
        img3 = cv2.imread(filesname[(phoneidstart+1)%sum],0)
        img4 = cv2.imread(filesname[(phoneidstart+2)%sum],0)
        
        img_open1 = Image.open(filesname[(phoneidstart-1)%sum])
        img_open2 = Image.open(filesname[phoneidstart%sum])
        img_open3 = Image.open(filesname[(phoneidstart+1)%sum])
        img_open4 = Image.open(filesname[(phoneidstart+2)%sum])
        
        if (img1.shape[0]>img1.shape[1]):
            img_open1 = img_open1.rotate(270,expand = True)
            img_open2 = img_open2.rotate(270,expand = True)
            img_open3 = img_open3.rotate(270,expand = True)
            img_open4 = img_open4.rotate(270,expand = True)

        #用于双击弹窗
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open2.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open3.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open4.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()

        if(flag==1):
            changemode()  
def previous_key(event):
    global phoneidstart
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale
    global phoneidstart
    global flag
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    global rect_box
    global group
    if(pathh.get() != ''):
        group -= 1
        sum = len(filesname)
        maxgroup = int(float(sum)/4+0.5)
        if(group<1):
            group = maxgroup
        string = 'sum:'+str(sum)+';group:'+str(group)
        tk.Label(window ,text=string).place(x=0.61*w_win, y=0.025*h_win, anchor='w')
        rect_box = [0,0,0,0]
        scale =maxscale
        box = (0, 0, w_canvas*scale, h_canvas*scale)    
        box2 = box
        box3 = box
        box4 = box

        # phoneidstart = (phoneidstart-4+sum)%sum
        # if(phoneidstart == 0):
        #     phoneidstart = sum
        phoneidstart -=4 
        if(phoneidstart <1):
            phoneidstart = (maxgroup-1)*4+1

        img1 = cv2.imread(filesname[(phoneidstart-1)%sum],0)
        img2 = cv2.imread(filesname[phoneidstart%sum],0)
        img3 = cv2.imread(filesname[(phoneidstart+1)%sum],0)
        img4 = cv2.imread(filesname[(phoneidstart+2)%sum],0)
        
        img_open1 = Image.open(filesname[(phoneidstart-1)%sum])
        img_open2 = Image.open(filesname[phoneidstart%sum])
        img_open3 = Image.open(filesname[(phoneidstart+1)%sum])
        img_open4 = Image.open(filesname[(phoneidstart+2)%sum])
        
        if (img1.shape[0]>img1.shape[1]):
            img_open1 = img_open1.rotate(270,expand = True)
            img_open2 = img_open2.rotate(270,expand = True)
            img_open3 = img_open3.rotate(270,expand = True)
            img_open4 = img_open4.rotate(270,expand = True)

        #用于双击弹窗
        whole_imagefile1 = ImageTk.PhotoImage(image = img_open1.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile2 = ImageTk.PhotoImage(image = img_open2.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile3 = ImageTk.PhotoImage(image = img_open3.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))
        whole_imagefile4 = ImageTk.PhotoImage(image = img_open4.resize((int(0.8*w_win),int(0.8*w_win*h_img/w_img))))

        image_file1 = create(img_open1,box)
        image_file2 = create(img_open2,box2)
        image_file3 = create(img_open3,box3)
        image_file4 = create(img_open4,box4)

        putimage()

        if(flag==1):
            changemode()     

#按钮upload绑定的函数，用于将四组打分数据暂存到全局的data二维数组中
#二维数组共六列
#自左至右依次为：场景id（senseid），手机编号（phoneID），图片绝对路径，打分区域，打分属性，分数
def upload():
    #global var1,var2,var3,var4
    global box,box2,box3,box4,scale
    global marktop
    global filesname
    global senseid,phoneidstart
    global data
    global flag #控制看图打分切换
    global rect_box,flag,rect1,rect2,rect3,rect4
    global cmb_flag,cmb2_flag
    global group
    # count+=1
    # qwer = tk.Label(window,font=('Arial', 12),bg='green')
    # qwer.place(x=0.67*w_win, y=0.025*h_win, anchor='w')
    # qwer["text"]=str(count)+"ok"
    cmb_flag = cmb['value'].index(cmb.get())
    cmb2_flag = cmb2['value'].index(cmb2.get())
    # print(cmb_flag)
    sum = len(filesname)
    maxgroup = int(float(sum)/4+0.5)
    #c为四个元组，代表4个框的位置
    #d为4个分数
    if(flag == 0):
        c = [box,box2,box3,box4]
    else:
        c_ori = [box,box2,box3,box4]
        c = []
        canvas1.delete(canvas1.find_withtag('rtag'))
        canvas2.delete(canvas2.find_withtag('rtag'))
        canvas3.delete(canvas3.find_withtag('rtag'))
        canvas4.delete(canvas4.find_withtag('rtag'))
        # lbox = list(box)
        # lbox2 = list(box2)
        # lbox3 = list(box3)
        # lbox4 = list(box4)
        if (rect_box == [0,0,0,0]):
            c = c_ori
        else:
            for i in range(4):
                lbox = list(c_ori[i])
                lbox[2] = lbox[0]+scale * rect_box[2]
                lbox[3] = lbox[1]+scale * rect_box[3]
                lbox[0] += scale * rect_box[0]
                lbox[1] += scale * rect_box[1]

                    
                tbox = tuple(lbox)
                c.append(tbox)


    d = [var1.get(),var2.get(),var3.get(),var4.get()]
    
    coverflag = 0
    coverloc = 0
    if (len(data) != 0):
        for j in range(len(data)):
            if data[j][1] == 4*group -3:
                coverloc = j
                coverflag = 1
                break
    
    if (group != maxgroup):
        for i in range(4):
            b = []
            b.append(senseid)
            tmp = phoneidstart + i
            if(tmp > sum):
                tmp = tmp%sum
            b.append(tmp)
            b.append(os.path.split(filesname[(i + phoneidstart -1)%sum])[-1])
            b.append(c[i])
            b.append(cmb.get())
            b.append(cmb2.get())
            b.append(d[i])
            # if(group != 4 or (group ==4 and i !=3)):
            if(coverflag == 1):       
                data[coverloc+i] = b
            else:
                data.append(b)
    else:
        rest = sum-4*(maxgroup-1)
        for i in range(rest):
            b = []
            b.append(senseid)
            tmp = phoneidstart + i
            if(tmp > sum):
                tmp = tmp%sum
            b.append(tmp)
            b.append(os.path.split(filesname[(i + phoneidstart -1)%sum])[-1])
            b.append(c[i])
            b.append(cmb.get())
            b.append(cmb2.get())
            b.append(d[i])
            # if(group != 4 or (group ==4 and i !=3)):
            if(coverflag == 1):       
                data[coverloc+i] = b
            else:
                data.append(b)

    rect_box = [0,0,0,0]
    var1.set(2.5) 
    var2.set(2.5) 
    var3.set(2.5) 
    var4.set(2.5) 
    if(flag==1):
        changemode()
    #tk.Label(window,text = "ok").place(x=0.55*w_win, y=0.025*h_win, anchor='w')
    marktop.destroy()
    print(data)

def upload_key(event):
    #global var1,var2,var3,var4
    global box,box2,box3,box4,scale
    global marktop
    global filesname
    global senseid,phoneidstart
    global data
    global flag #控制看图打分切换
    global rect_box,flag,rect1,rect2,rect3,rect4
    global cmb_flag,cmb2_flag
    global group
    # count+=1
    # qwer = tk.Label(window,font=('Arial', 12),bg='green')
    # qwer.place(x=0.67*w_win, y=0.025*h_win, anchor='w')
    # qwer["text"]=str(count)+"ok"
    cmb_flag = cmb['value'].index(cmb.get())
    cmb2_flag = cmb2['value'].index(cmb2.get())
    # print(cmb_flag)
    sum = len(filesname)
    maxgroup = int(float(sum)/4+0.5)
    #c为四个元组，代表4个框的位置
    #d为4个分数
    if(flag == 0):
        c = [box,box2,box3,box4]
    else:
        c_ori = [box,box2,box3,box4]
        c = []
        canvas1.delete(canvas1.find_withtag('rtag'))
        canvas2.delete(canvas2.find_withtag('rtag'))
        canvas3.delete(canvas3.find_withtag('rtag'))
        canvas4.delete(canvas4.find_withtag('rtag'))
        # lbox = list(box)
        # lbox2 = list(box2)
        # lbox3 = list(box3)
        # lbox4 = list(box4)
        if (rect_box == [0,0,0,0]):
            c = c_ori
        else:
            for i in range(4):
                lbox = list(c_ori[i])
                lbox[2] = lbox[0]+scale * rect_box[2]
                lbox[3] = lbox[1]+scale * rect_box[3]
                lbox[0] += scale * rect_box[0]
                lbox[1] += scale * rect_box[1]

                    
                tbox = tuple(lbox)
                c.append(tbox)


    d = [var1.get(),var2.get(),var3.get(),var4.get()]
    
    coverflag = 0
    coverloc = 0
    if (len(data) != 0):
        for j in range(len(data)):
            if data[j][1] == 4*group -3:
                coverloc = j
                coverflag = 1
                break
    
    if (group != maxgroup):
        for i in range(4):
            b = []
            b.append(senseid)
            tmp = phoneidstart + i
            if(tmp > sum):
                tmp = tmp%sum
            b.append(tmp)
            b.append(os.path.split(filesname[(i + phoneidstart -1)%sum])[-1])
            b.append(c[i])
            b.append(cmb.get())
            b.append(cmb2.get())
            b.append(d[i])
            # if(group != 4 or (group ==4 and i !=3)):
            if(coverflag == 1):       
                data[coverloc+i] = b
            else:
                data.append(b)
    else:
        rest = sum-4*(maxgroup-1)
        for i in range(rest):
            b = []
            b.append(senseid)
            tmp = phoneidstart + i
            if(tmp > sum):
                tmp = tmp%sum
            b.append(tmp)
            b.append(os.path.split(filesname[(i + phoneidstart -1)%sum])[-1])
            b.append(c[i])
            b.append(cmb.get())
            b.append(cmb2.get())
            b.append(d[i])
            # if(group != 4 or (group ==4 and i !=3)):
            if(coverflag == 1):       
                data[coverloc+i] = b
            else:
                data.append(b)

    rect_box = [0,0,0,0]
    var1.set(2.5) 
    var2.set(2.5) 
    var3.set(2.5) 
    var4.set(2.5) 
    if(flag==1):
        changemode()
    #tk.Label(window,text = "ok").place(x=0.55*w_win, y=0.025*h_win, anchor='w')
    marktop.destroy()
    print(data)


#用于提交最终打分结果
#两个部分：将全局的data数据输出为json或csv文件
def save():
    global path
    global data
    global senseid
    global cmb
    #data = data[:15]
    if (data != []):
        temp = np.array(data) 
        temp1 = temp[np.lexsort(temp.T)]
        data = temp1.tolist() 
        # data = sorted(data)
        jsonfile=open(path+'/'+senseid+data[0][4]+'.json','w')
        dataa = []
        for i in range(len(data)):
            senseid = data[i][0]
            phoneid = data[i][1]
            realpath = data[i][2]
            area = data[i][3]
            attribute = data[i][4]
            subattribute = data[i][5]
            score = data[i][6]

            content = []
            a = dict()
            a['area'] = area
            a['attribute'] = attribute
            a['subattribute'] = subattribute
            a['score'] = score
            content.append(a)

            h = dict()
            h['senseid'] = senseid
            h['phoneid'] = phoneid
            h['path'] = realpath
            h['content'] = content
            dataa.append(h)
        d=dict()
        d['data']=dataa 
        json.dump(d,jsonfile)

        
        name_attribute = ['senseid','phoneid','path','area','arrtibute','subattribute','score']
        csvFile = open(path+'/'+senseid+data[0][4]+'.csv', "w",newline='')
        writer = csv.writer(csvFile)
        writer.writerow(name_attribute)
        for i in range(len(data)):
            writer.writerow(data[i])
        data = []
        tkinter.messagebox.showwarning(message='保存成功')  
def save_key(event):
    global path
    global data
    global senseid
    global cmb
    if (data!=[]):
        #data = data[:15]
        temp = np.array(data) 
        temp1 = temp[np.lexsort(temp.T)]
        data = temp1.tolist() 
        # data = sorted(data)
        jsonfile=open(path+'/'+senseid+data[0][4]+'.json','w')
        dataa = []
        for i in range(len(data)):
            senseid = data[i][0]
            phoneid = data[i][1]
            realpath = data[i][2]
            area = data[i][3]
            attribute = data[i][4]
            subattribute = data[i][5]
            score = data[i][6]

            content = []
            a = dict()
            a['area'] = area
            a['attribute'] = attribute
            a['subattribute'] = subattribute
            a['score'] = score
            content.append(a)

            h = dict()
            h['senseid'] = senseid
            h['phoneid'] = phoneid
            h['path'] = realpath
            h['content'] = content
            dataa.append(h)
        d=dict()
        d['data']=dataa 
        json.dump(d,jsonfile)

        
        name_attribute = ['senseid','phoneid','path','area','arrtibute','subattribute','score']
        csvFile = open(path+'/'+senseid+data[0][4]+'.csv', "w",newline='')
        writer = csv.writer(csvFile)
        writer.writerow(name_attribute)
        for i in range(len(data)):
            writer.writerow(data[i])
        data = []
        tkinter.messagebox.showwarning(message='保存成功') 



def changemode():
    global flag
    global rect1,rect2,rect3,rect4,rect_box
    if(pathh.get() != ''):
        rect_box = [0,0,0,0]
        if(flag == 0):
            flag = 1
            changeb['text'] = '关闭框选打分'
            #update()
        else:
            flag = 0
            changeb['text'] = '启用框选打分'
            canvas1.delete(canvas1.find_withtag('rtag'))
            canvas2.delete(canvas2.find_withtag('rtag'))
            canvas3.delete(canvas3.find_withtag('rtag'))
            canvas4.delete(canvas4.find_withtag('rtag'))
        #print(flag)

#双击弹窗查看图片的实现
#一定要在画布区域双击，不然没用
#双击哪一张，哪一张全屏展示
#此函数有坑，imagefile一定要在函数之外准备好，函数内部做是不行的
#参考： https://blog.csdn.net/echoshoot/article/details/60882523 
def display(event):
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4
    global h_win,w_win,w_img,h_img
    global top
    global whichpic
    if(pathh.get() != ''):
        if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):
            try:
                top.destroy()    
            finally:
                top = tk.Toplevel(window,takefocus=True)
            #if (event.widget == canvas1 ):
            # dis_img = ImageTk.PhotoImage(image = img_open1)
            #top = tk.Toplevel()
            #int(0.8*w_win)  int(0.8*w_win*h_img/w_img)
            top.focusmodel(model="passive")
            abc = str(int(w_win))+'x'+ str(int(h_win))
            top.geometry(abc) 
            # Lab= tk.Label(top,image= whole_imagefile1)
            # Lab.place(x = 0,y = 0, anchor='nw')
            
            dis_canvas = tk.Canvas(top,height=0.9*h_win, width=0.9*w_win)
            if (event.widget == canvas1 ):
                img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile1) 
                whichpic = 1    
            if (event.widget == canvas2 ):
                img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile2)  
                whichpic = 2 
            if (event.widget == canvas3 ):
                img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile3) 
                whichpic = 3  
            if (event.widget == canvas4 ):
                img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile4)   
                whichpic = 4
            dis_canvas.place(x=0.5*w_win, y=0.5*h_win, anchor='center')
            tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0*w_win, y=0.5*h_win, anchor='w')
            tk.Button(top, text = "next", command = nextpic).place(x=0.95*w_win, y=0.5*h_win, anchor='w')
            top.bind('<Right>',key_nextpic)

#该函数用于在展示全图的时候，切换下一张  
def nextpic():
    global whichpic
    global top
    
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4
    global h_win,w_win,w_img,h_img
    # #if (event.widget == canvas1 ):
    # # dis_img = ImageTk.PhotoImage(image = img_open1)
    # top = tk.Toplevel()
    # #int(0.8*w_win)  int(0.8*w_win*h_img/w_img)
    # abc = str(int(w_win))+'x'+ str(int(h_win))
    # top.geometry(abc) 
    # # Lab= tk.Label(top,image= whole_imagefile1)
    # # Lab.place(x = 0,y = 0, anchor='nw')
    whichpic = (whichpic+1)%4
    if(whichpic==0):
        whichpic =4
    dis_canvas = tk.Canvas(top,height=0.9*h_win, width=0.9*w_win)
    if (whichpic == 1 ):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile1)     
    if (whichpic == 2):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile2)   
    if (whichpic == 3):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile3)   
    if (whichpic == 4):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile4)   
    dis_canvas.place(x=0.5*w_win, y=0.5*h_win, anchor='center')
    #label1.delete()
    tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0, y=0.5*h_win, anchor='w')
def key_nextpic(event):
    global whichpic
    global top
    
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4
    global h_win,w_win,w_img,h_img
    # #if (event.widget == canvas1 ):
    # # dis_img = ImageTk.PhotoImage(image = img_open1)
    # top = tk.Toplevel()
    # #int(0.8*w_win)  int(0.8*w_win*h_img/w_img)
    # abc = str(int(w_win))+'x'+ str(int(h_win))
    # top.geometry(abc) 
    # # Lab= tk.Label(top,image= whole_imagefile1)
    # # Lab.place(x = 0,y = 0, anchor='nw')
    whichpic = (whichpic+1)%4
    if(whichpic==0):
        whichpic =4
    dis_canvas = tk.Canvas(top,height=0.9*h_win, width=0.9*w_win)
    if (whichpic == 1 ):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile1)     
    if (whichpic == 2):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile2)   
    if (whichpic == 3):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile3)   
    if (whichpic == 4):
        img = dis_canvas.create_image(0.5*w_win, 0.5*h_win, anchor='center',image=whole_imagefile4)   
    dis_canvas.place(x=0.5*w_win, y=0.5*h_win, anchor='center')
    #label1.delete()
    tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0, y=0.5*h_win, anchor='w')
def marking(event):
    global marktop
    global var1,var2,var3,var4,cmb2,cmb
    global insimagefile
    global cmb_flag,cmb2_flag
    global group
    if(pathh.get() != ''):
        try:
            marktop.destroy()    
        finally:
            marktop = tk.Toplevel(window,takefocus=True)
        #abc = str(int(w_win*0.2))+'x'+ str(int(h_win*0.2))
        marktop.geometry('{}x{}+{}+{}'.format(int(w_win*0.2),int(h_win*0.28), int(w_win*0.4), int(h_win*0.36))) 

        tk.Label(marktop,text='评分属性：').place(x=0, y=0, anchor='nw')
        cmb = ttk.Combobox(marktop)
        cmb.place(x=0.04*w_win, y=0, anchor='nw')
        # 设置下拉菜单中的值
        cmb['value'] = ('Exposure','Color','Texture','Noise','AF')
        cmb['state'] = 'readonly'
        cmb.current(cmb_flag)
        cmb.bind("<<ComboboxSelected>>",change_cmb2)

        cmb2 = ttk.Combobox(marktop)
        cmb2.place(x=0.04*w_win, y=0.04*h_win, anchor='nw')
        # 设置下拉菜单中的值
        if(cmb.get() == 'Color'):
            cmb2['value'] = ('AWB','ColorRendering','ColorShading','颜色一致性')
        elif(cmb.get() == 'Texture'):
            cmb2['value'] = ('静止三脚架/运动手持')
        elif(cmb.get() == 'Noise'):
            cmb2['value'] = ('亮度噪声','彩色噪声')
        elif(cmb.get() == 'AF'):
            cmb2['value'] = ('对焦一致性')
        else:
            cmb2['value'] = ('Exposure Target','HDR','对比度','亮度一致性')
        cmb2['state'] = 'readonly'
        cmb2.current(cmb2_flag)

        tk.Label(marktop,text=group).place(x=0.15*w_win, y=0.05*h_win, anchor='w')
        tk.Label(marktop,text='1',bg='green').place(x=0, y=0.1*h_win, anchor='w')
        var1 = tk.DoubleVar()  
        var1.set(2.5) 
        #mark1 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var1 ,length = 300,showvalue=1,tickinterval=0.5)
        mark1 = tk.Scale(marktop,from_=0,  to=5,  resolution=0.1, orient=tk.HORIZONTAL , variable=var1 ,length = int(w_win*0.185),showvalue=0,tickinterval=0.5)
        mark1.place(x=0.01*w_win, y=0.1*h_win, anchor='w')

        tk.Label(marktop,text='2',bg='green').place(x=0, y=0.14*h_win, anchor='w')
        var2 = tk.DoubleVar()
        var2.set(2.5) 
        mark2 = tk.Scale(marktop,from_=0,  to=5,  resolution=0.1, orient=tk.HORIZONTAL , variable=var2,length = int(w_win*0.185),showvalue=0,tickinterval=0.5)
        mark2.place(x=0.01*w_win, y=0.14*h_win, anchor='w')

        tk.Label(marktop,text='3',bg='green').place(x=0, y=0.18*h_win, anchor='w')
        var3 = tk.DoubleVar()  
        var3.set(2.5) 
        mark3 = tk.Scale(marktop,from_=0,  to=5,  resolution=0.1, orient=tk.HORIZONTAL , variable=var3,length = int(w_win*0.185),showvalue=0,tickinterval=0.5)
        mark3.place(x=0.01*w_win, y=0.18*h_win, anchor='w')

        tk.Label(marktop,text='4',bg='green').place(x=0, y=0.222*h_win, anchor='w')
        var4 = tk.DoubleVar() 
        var4.set(2.5) 
        mark4 = tk.Scale(marktop,from_=0,  to=5,  resolution=0.1, orient=tk.HORIZONTAL , variable=var4,length = int(w_win*0.185),showvalue=0,tickinterval=0.5)
        mark4.place(x=0.01*w_win, y=0.222*h_win, anchor='w')

        b = tk.Button(marktop, text='上传打分（Ctrl+u）',  command=upload)
        b.place(x=0.1*w_win, y=0.245*h_win, anchor='n')

        Lab= tk.Label(marktop,image= insimagefile)
        Lab.place(x=0.2*w_win, y=0, anchor='ne')

        marktop.bind('<Control-Key-u>',upload_key)

def change_cmb2(event):
    global cmb2
    #global cmb_flag,cmb2_flag

    cmb2 = ttk.Combobox(marktop)
    cmb2.place(x=0.04*w_win, y=0.04*h_win, anchor='nw')
    if(cmb.get() == 'Color'):
        cmb2['value'] = ('AWB','ColorRendering','ColorShading','颜色一致性')
    elif(cmb.get() == 'Texture'):
        cmb2['value'] = ('静止三脚架/运动手持')
    elif(cmb.get() == 'Noise'):
        cmb2['value'] = ('亮度噪声','彩色噪声')
    elif(cmb.get() == 'AF'):
        cmb2['value'] = ('对焦一致性')
    else:
        cmb2['value'] = ('Exposure Target','HDR动态范围','对比度','亮度一致性')
    cmb2['state'] = 'readonly'
    cmb2.current(0)

window.title('My Window')



insimgopen = Image.open('1.png')  #用于打分时提示1234
# print(insimgopen)
# region = insimgopen.resize((100, 80))
insimagefile = ImageTk.PhotoImage(image = insimgopen)

w_win = window.winfo_screenwidth()
h_win = window.winfo_screenheight()

#print(w_win,h_win)
big = str(w_win) + 'x' + str(h_win)
window.geometry(big) 

w_canvas =int(w_win*0.5)
h_canvas = int(h_win*0.47)


phoneidstart = 1   #1,5,9....
whichpic = 1  #for toplevel display
data = [] #缓存数据

flag = 0 #用于控制打分类型，0为直接打分，1为框选打分
cmb_flag = 0
cmb2_flag = 0 #记录上次打分选择的属性是第几个，方便下次打分
ctrlflag = 0 #用于单独拖动，0为一起，1为单独
rect_box = [0,0,0,0]  #用于记录矩形位置,画布上的相对位置，而非真实位置

pathh = tk.StringVar()  #无需global
tk.Label(window,text = "目标路径:").place(x=0.0*w_win, y=0.025*h_win, anchor='w')
tk.Entry(window, textvariable = pathh).place(x=0.035*w_win, y=0.025*h_win,width = 251, anchor='w')
tk.Button(window, text = "路径选择", command = selectPath).place(x=0.2*w_win, y=0.025*h_win, anchor='w')

loc = [] #用于drag

changeb = tk.Button(window, text='启用框选打分',  command=changemode)
changeb.place(x=0.51*w_win, y=0.025*h_win, anchor='w')

canvas1 = tk.Canvas(window, height=h_canvas, width=w_canvas)
#image1 = canvas1.create_image(w_canvas, h_canvas, anchor='se',image=image_file1)  
canvas1.place(x=0.5*w_win, y=0.52*h_win, anchor='se')

canvas2 = tk.Canvas(window,height=h_canvas, width=w_canvas)
#image2 = canvas2.create_image(0, h_canvas, anchor='sw',image=image_file2)     
canvas2.place(x=0.5*w_win, y=0.52*h_win, anchor='sw')

canvas3 = tk.Canvas(window, height=h_canvas, width=w_canvas)
#image3 = canvas3.create_image(w_canvas, 0, anchor='ne',image=image_file3)     
canvas3.place(x=0.5*w_win, y=0.52*h_win, anchor='ne')

canvas4 = tk.Canvas(window, height=h_canvas, width=w_canvas)
#image4 = canvas4.create_image(0, 0, anchor='nw',image=image_file4)  
canvas4.place(x=0.5*w_win, y=0.52*h_win, anchor='nw')



b0= tk.Button(window, text='对齐(ctrl+m)', font=('Arial', 12),command=update)
b0.place(x=0.41*w_win, y=0.025*h_win, anchor='w')
#b0.bind('<Control-Key-m>')




b3= tk.Button(window, text='上一组(crtl+ ← )', font=('Arial', 12),command=previous)
b3.place(x=0.71*w_win, y=0.025*h_win, anchor='w')

b2= tk.Button(window, text='下一组(crtl+ → )', font=('Arial', 12),command=next)
b2.place(x=0.81*w_win, y=0.025*h_win, anchor='w')

b1= tk.Button(window, text='保存(ctrl+s)', font=('Arial', 12),command=save)
b1.place(x=0.91*w_win, y=0.025*h_win, anchor='w')

b4= tk.Button(window, text='判断', font=('Arial', 12),command=judge_gray)
b4.place(x=0.86*w_win, y=0.025*h_win, anchor='w')

Labins= tk.Label(window,text= "请先选择路径",font=('Arial', 12))
Labins.place(x=0.5*w_win, y=0.5*h_win, anchor='center')


window.bind("<MouseWheel>",scaler)
window.bind("<Button-4>",scaler)
window.bind("<Button-5>",scaler)
window.bind("<B1-Motion>",drag)
window.bind("<ButtonRelease-1>",locclear)
window.bind('<Control-Key-m>',update_key)
# window.bind('<Control-Key-u>',upload_key)
window.bind('<Control-Key-s>',save_key)
window.bind('<Double-Button-1>',display)
window.bind('<Control-Right>',next_key)
window.bind('<Control-Left>',previous_key)
window.bind("<3>",marking)
window.bind("<KeyPress-Control_L>",kpc)
window.bind("<KeyRelease-Control_L>",krc)

#window.attributes("-topmost",True)
window.mainloop()

#https://github.com/Twang1998/markGUI