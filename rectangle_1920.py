
import cv2
from PIL import Image, ImageTk
import numpy as np
import tkinter.filedialog
import tkinter as tk 
import os
import threading
import time
from tkinter import ttk
import json
import csv

import tkinter.messagebox 

window = tk.Tk()   #创建根窗口
 
top = tk.Toplevel(window)   #创建顶层窗口，用于在双击时弹窗显示点击的图片
top.destroy()   #顶层窗口暂时不用，双击时才会弹出

#该函数通过文件夹的路径path可以生成一个数组，数组的元素均为文件夹下每一张图片的绝对路径
def getfilesname(path):
    filesname =[]
    if(path != ''):
        dirs = os.listdir(path)
        for i in dirs:
            if os.path.splitext(i)[1] == ".jpg" or os.path.splitext(i)[1] == ".png" or os.path.splitext(i)[1] == ".JPG" or os.path.splitext(i)[1] == ".jpeg":
                filesname+=[path+'/'+i]
    else:
        filesname = []
    return filesname

#该函数用于切换文件夹，当“选择路径”按钮按下时出发
#该函数包含众多全局变量，并对其一一修改
def selectPath():
    global pathh
    global path
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
    
    data = []  #这两行用于单独存放
    path = tkinter.filedialog.askdirectory() 
    filesname = getfilesname(path)

    #判断文件夹是否合法
    while(len(filesname) == 0 or len(filesname)%4 != 0):
        path = tkinter.filedialog.askdirectory()
    pathh.set(path)
    filesname = getfilesname(path)
    senseid += 1
    phoneidstart = 1

    # #用于match算法
    img1 = cv2.imread(filesname[0],0)
    img2 = cv2.imread(filesname[1],0)
    img3 = cv2.imread(filesname[2],0)
    img4 = cv2.imread(filesname[3],0)
    
    img_open1 = Image.open(filesname[0])
    img_open2 = Image.open(filesname[1])
    img_open3 = Image.open(filesname[2])
    img_open4 = Image.open(filesname[3])
    # img1 = cv2.cvtColor(np.asarray(img_open1), cv2.COLOR_RGB2BGR)
    # img2 = cv2.cvtColor(np.asarray(img_open2), cv2.COLOR_RGB2BGR)
    # img3 = cv2.cvtColor(np.asarray(img_open3), cv2.COLOR_RGB2BGR)
    # img4 = cv2.cvtColor(np.asarray(img_open4), cv2.COLOR_RGB2BGR)
    #print(img1.shape[1])
    if (img1.shape[0]>img1.shape[1]):
        img_open1 = img_open1.rotate(270,expand = True)
        img_open2 = img_open2.rotate(270,expand = True)
        img_open3 = img_open3.rotate(270,expand = True)
        img_open4 = img_open4.rotate(270,expand = True)
    #https://blog.csdn.net/mizhenpeng/article/details/82794112

    w_img = img1.shape[1]
    h_img = img1.shape[0]
    
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
def print_selection():
    print('you have selected ' + var.get())

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
    global image1,image2,image3,image4
    global box
    global w_canvas,h_canvas,maxscale

    canvas1.delete(image1)
    canvas2.delete(image2)
    canvas3.delete(image3)
    canvas4.delete(image4)


    image1 = canvas1.create_image(w_canvas, h_canvas, anchor='se',image=image_file1)  

    image2 = canvas2.create_image(0, h_canvas, anchor='sw',image=image_file2)     

    image3 = canvas3.create_image(w_canvas, 0, anchor='ne',image=image_file3)     

    image4 = canvas4.create_image(0, 0, anchor='nw',image=image_file4)  


#用于实现拖动功能
#只有在canvas上拖动才有意义（对应第一个if语句）
# 设计思路：左键按下，开始拖动，进入函数，然后不停的将鼠标当前位置（event.x，event.y）记录到全局变量loc中
# 进而判断拖动方向，修改box，实现拖动    
def drag(event):
    global box,box2,box3,box4
    global img1,img2,img3,img4
    global image_file1,image_file2,image_file3,image_file4
    global rect1,rect2,rect3,rect4
    global loc
    global scale
    global w_canvas,h_canvas,maxscale
    global flag
    global rect_box
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
            if (len(loc) == 2):
                if boxx[0]+(loc[0][0]-loc[1][0])*scale<=0:
                    boxx[0] = 0
                elif boxx[0]+(loc[0][0]-loc[1][0])*scale>= w_img-w_canvas*scale:
                    boxx[0] = w_img-w_canvas*scale
                else:
                    boxx[0] = boxx[0]+(loc[0][0]-loc[1][0])*scale

                if boxx[1]+(loc[0][1]-loc[1][1])*scale <= 0:
                    boxx[1] = 0
                elif boxx[1]+(loc[0][1]-loc[1][1])*scale>= h_img-h_canvas*scale:
                    boxx[1]= h_img-h_canvas*scale
                else:
                    boxx[1] = boxx[1]+(loc[0][1]-loc[1][1])*scale

                boxx[2] = boxx[0] +w_canvas*scale
                boxx[3] = boxx[1] +h_canvas*scale

                box = tuple(boxx)

                box2 = box
                box3 = box
                box4 = box
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
                canvas1.delete(rect1)
                canvas2.delete(rect2)
                canvas3.delete(rect3)
                canvas4.delete(rect4)

                rect1 = canvas1.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3)
                rect2 = canvas2.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3)
                rect3 = canvas3.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3)
                rect4 = canvas4.create_rectangle(loc[0][0], loc[0][1], loc[1][0], loc[1][1],outline='pink',width=3)

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
    if (flag==0):
        if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):
            boxx = list(box)

            oldscale = scale

            if(event.delta > 0 and oldscale >1):
                scale = max(oldscale-1,1)
                boxx[0] = boxx[0] + event.x
                boxx[1] = boxx[1] + event.y
        
            if(event.delta < 0 and oldscale < maxscale):
                scale = min(oldscale+1,maxscale)
                if (boxx[0] - event.x <0):
                    boxx[0]=0
                elif(boxx[0] - event.x > w_img-w_canvas*scale):
                    boxx[0]=w_img-w_canvas*scale
                else:
                    boxx[0] = boxx[0] - event.x
                
                if (boxx[1] - event.y <0):
                    boxx[1]=0
                elif(boxx[1] - event.y > h_img-h_canvas*scale):
                    boxx[1]=h_img-h_canvas*scale
                else:
                    boxx[1] = boxx[1] - event.y


            boxx[2] = boxx[0]+w_canvas*scale
            boxx[3] = boxx[1]+h_canvas*scale
        
            box = tuple(boxx)
            box2 = box
            box3 = box
            box4 = box
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
def match(img1,img2,box1):
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

#Ctrl+m 触发该函数
#实现图片对齐，其中调用三次match函数
#按钮 match 触发该函数
#实现图片对齐，其中调用三次match函数
def update():
    global box,box2,box3,box4
    global img1,img2,img3,img4,flag
    global image_file1,image_file2,image_file3,image_file4

    box2 = match(img1,img2,box)
    box3 = match(img1,img3,box)
    box4 = match(img1,img4,box)

    image_file1 = create(img_open1,box)
    image_file2 = create(img_open2,box2)
    image_file3 = create(img_open3,box3)
    image_file4 = create(img_open4,box4)

    putimage()
def update_key(event):
    global box,box2,box3,box4
    global img1,img2,img3,img4,flag
    global image_file1,image_file2,image_file3,image_file4

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
    global flag
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    scale =maxscale
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box

    phoneidstart += 4
    if (phoneidstart <= len(filesname)):
        img1 = cv2.imread(filesname[phoneidstart-1],0)
        img2 = cv2.imread(filesname[phoneidstart],0)
        img3 = cv2.imread(filesname[phoneidstart+1],0)
        img4 = cv2.imread(filesname[phoneidstart+2],0)
        
        img_open1 = Image.open(filesname[phoneidstart-1])
        img_open2 = Image.open(filesname[phoneidstart])
        img_open3 = Image.open(filesname[phoneidstart+1])
        img_open4 = Image.open(filesname[phoneidstart+2])


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
    else:
        phoneidstart -= 4
        a = tkinter.messagebox.showwarning(message='此文件夹已结束')
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
    global flag
    global whole_imagefile1,whole_imagefile2,whole_imagefile3,whole_imagefile4,w_win,h_win,w_img,h_img #用于双击弹窗
    scale =maxscale
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box

    phoneidstart += 4
    if (phoneidstart <= len(filesname)):
        img1 = cv2.imread(filesname[phoneidstart-1],0)
        img2 = cv2.imread(filesname[phoneidstart],0)
        img3 = cv2.imread(filesname[phoneidstart+1],0)
        img4 = cv2.imread(filesname[phoneidstart+2],0)
        
        img_open1 = Image.open(filesname[phoneidstart-1])
        img_open2 = Image.open(filesname[phoneidstart])
        img_open3 = Image.open(filesname[phoneidstart+1])
        img_open4 = Image.open(filesname[phoneidstart+2])


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
    else:
        phoneidstart -= 4
        tkinter.messagebox.showwarning(message='此文件夹已结束')
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
    scale =maxscale
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box

    phoneidstart -= 4
    if (phoneidstart >= 1):
        img1 = cv2.imread(filesname[phoneidstart-1],0)
        img2 = cv2.imread(filesname[phoneidstart],0)
        img3 = cv2.imread(filesname[phoneidstart+1],0)
        img4 = cv2.imread(filesname[phoneidstart+2],0)
        
        img_open1 = Image.open(filesname[phoneidstart-1])
        img_open2 = Image.open(filesname[phoneidstart])
        img_open3 = Image.open(filesname[phoneidstart+1])
        img_open4 = Image.open(filesname[phoneidstart+2])


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
    else:
        phoneidstart += 4
        a = tkinter.messagebox.showwarning(message='这已经是第一组场景！')
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
    scale =maxscale
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box

    phoneidstart -= 4
    if (phoneidstart >= 1):
        img1 = cv2.imread(filesname[phoneidstart-1],0)
        img2 = cv2.imread(filesname[phoneidstart],0)
        img3 = cv2.imread(filesname[phoneidstart+1],0)
        img4 = cv2.imread(filesname[phoneidstart+2],0)
        
        img_open1 = Image.open(filesname[phoneidstart-1])
        img_open2 = Image.open(filesname[phoneidstart])
        img_open3 = Image.open(filesname[phoneidstart+1])
        img_open4 = Image.open(filesname[phoneidstart+2])


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
    else:
        phoneidstart += 4
        tkinter.messagebox.showwarning(message='这已经是第一组场景!')
    if(flag==1):
        changemode()  

#按钮upload绑定的函数，用于将四组打分数据暂存到全局的data二维数组中
#二维数组共六列
#自左至右依次为：场景id（senseid），手机编号（phoneID），图片绝对路径，打分区域，打分属性，分数
def upload():
    #global var1,var2,var3,var4
    global box,box2,box3,box4,scale
    global filesname
    global senseid,phoneidstart
    global data
    global count,flag
    global rect_box,flag,rect1,rect2,rect3,rect4
    count+=1
    qwer = tk.Label(window,font=('Arial', 12),bg='green')
    qwer.place(x=0.67*w_win, y=0.025*h_win, anchor='w')
    qwer["text"]=str(count)+"ok"
    if(flag == 0):
        c = [box,box2,box3,box4]
    else:
        c_ori = [box,box2,box3,box4]
        c = []
        canvas1.delete(rect1)
        canvas2.delete(rect2)
        canvas3.delete(rect3)
        canvas4.delete(rect4)
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
    
    for i in range(4):
        b = []
        b.append(senseid)
        b.append(phoneidstart + i)
        b.append(filesname[i + phoneidstart -1])
        b.append(c[i])
        b.append(cmb.get())
        b.append(d[i])
        data.append(b)
    rect_box = [0,0,0,0]
    var1.set(2.5) 
    var2.set(2.5) 
    var3.set(2.5) 
    var4.set(2.5) 
    if(flag==1):
        changemode()
    #tk.Label(window,text = "ok").place(x=0.55*w_win, y=0.025*h_win, anchor='w')
    print(data)
def upload_key(event):
    #global var1,var2,var3,var4
    global box,box2,box3,box4,scale
    global filesname
    global senseid,phoneidstart
    global data
    global count
    global flag
    global rect_box,flag,rect1,rect2,rect3,rect4
    count+=1
    qwer = tk.Label(window,font=('Arial', 12),bg='green')
    qwer.place(x=0.67*w_win, y=0.025*h_win, anchor='w')
    qwer["text"]=str(count)+"ok"
    if(flag == 0):
        c = [box,box2,box3,box4]
    else:
        c_ori = [box,box2,box3,box4]
        c = []
        canvas1.delete(rect1)
        canvas2.delete(rect2)
        canvas3.delete(rect3)
        canvas4.delete(rect4)
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
    
    for i in range(4):
        b = []
        b.append(senseid)
        b.append(phoneidstart + i)
        b.append(filesname[i + phoneidstart -1])
        b.append(c[i])
        b.append(cmb.get())
        b.append(d[i])
        data.append(b)
    rect_box = [0,0,0,0]
    var1.set(2.5) 
    var2.set(2.5) 
    var3.set(2.5) 
    var4.set(2.5) 
    if(flag==1):
        changemode()
    #tk.Label(window,text = "ok").place(x=0.55*w_win, y=0.025*h_win, anchor='w')
    print(data)

#用于提交最终打分结果
#两个部分：将全局的data数据输出为json或csv文件
def save():
    global path
    global data
    global senseid
    data = sorted(data)
    jsonfile=open(path+'/sense'+str(senseid)+'.json','w')
    dataa = []
    for i in range(len(data)):
        senseid = data[i][0]
        phoneid = data[i][1]
        realpath = data[i][2]
        area = data[i][3]
        attribute = data[i][4]
        score = data[i][5]

        content = []
        a = dict()
        a['area'] = area
        a['attribute'] = attribute
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

    
    name_attribute = ['senseid','phoneid','path','area','arrtibute','score']
    csvFile = open(path+'/sense'+str(senseid)+'.csv', "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow(name_attribute)
    for i in range(len(data)):
        writer.writerow(data[i])
    
    tkinter.messagebox.showwarning(message='保存成功')  

def save_key(event):
    global path
    global data
    data = sorted(data)
    jsonfile=open(path+'/sense'+str(senseid)+'.json','w')
    dataa = []
    for i in range(len(data)):
        senseid = data[i][0]
        phoneid = data[i][1]
        realpath = data[i][2]
        area = data[i][3]
        attribute = data[i][4]
        score = data[i][5]

        content = []
        a = dict()
        a['area'] = area
        a['attribute'] = attribute
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

    
    name_attribute = ['senseid','phoneid','path','area','arrtibute','score']
    csvFile = open(path+'/sense'+str(senseid)+'.csv', "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow(name_attribute)
    for i in range(len(data)):
        writer.writerow(data[i])
    
    tkinter.messagebox.showwarning(message='保存成功')  


def changemode():
    global flag
    global rect1,rect2,rect3,rect4,rect_box
    rect_box = [0,0,0,0]
    if(flag == 0):
        flag = 1
        changeb['text'] = '关闭框选打分'
        #update()
    else:
        flag = 0
        changeb['text'] = '启用框选打分'
        canvas1.delete(rect1)
        canvas2.delete(rect2)
        canvas3.delete(rect3)
        canvas4.delete(rect4)
    print(flag)

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
        tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0.05*w_win, y=0.05*h_win, anchor='se')
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
    tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0.05*w_win, y=0.1*h_win, anchor='se')
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
    tk.Label(top,text = whichpic,bg='green',font=('Arial', 50)).place(x=0.05*w_win, y=0.1*h_win, anchor='se')  



window.title('My Window')

w_win = window.winfo_screenwidth()
h_win = window.winfo_screenheight()

print(w_win,h_win)
big = str(w_win) + 'x' + str(h_win)
window.geometry(big) 

w_canvas =int(w_win*0.5)
h_canvas = int(h_win*0.43)
count=0
senseid = 1
phoneidstart = 1
whichpic = 1  #for toplevel
data = []

flag = 0 #用于控制打分类型，0为直接打分，1为框选打分
rect_box = [0,0,0,0]  #用于记录矩形位置,画布上的相对位置，而非真实位置


#path = 'C:/Users/37151/Desktop/tkinter/sense1'
path = os.getcwd() + '/sense1'
path=path.replace("\\","/")
print(path)
pathh = tk.StringVar()
tk.Label(window,text = "目标路径:").place(x=0.0*w_win, y=0.025*h_win, anchor='w')
tk.Entry(window, textvariable = pathh).place(x=0.035*w_win, y=0.025*h_win,width = 251, anchor='w')
tk.Button(window, text = "路径选择", command = selectPath).place(x=0.2*w_win, y=0.025*h_win, anchor='w')

filesname=getfilesname(path)

img1 = cv2.imread(filesname[0],0)
img2 = cv2.imread(filesname[1],0)
img3 = cv2.imread(filesname[2],0)
img4 = cv2.imread(filesname[3],0)

img_open1 = Image.open(filesname[0])
img_open2 = Image.open(filesname[1])
img_open3 = Image.open(filesname[2])
img_open4 = Image.open(filesname[3])

if (img1.shape[0]>img1.shape[1]):
    img_open1 = img_open1.rotate(270)
    img_open2 = img_open2.rotate(270)
    img_open3 = img_open3.rotate(270)
    img_open4 = img_open4.rotate(270)

w_img = img1.shape[1]
h_img = img1.shape[0]

maxscale = min(int(w_img/w_canvas),int(h_img/h_canvas))

scale = maxscale

loc = []

box = (0, 0, w_canvas*scale, h_canvas*scale)  
box2 = (0, 0, w_canvas*scale, h_canvas*scale)
box3 = (0, 0, w_canvas*scale, h_canvas*scale)
box4 = (0, 0, w_canvas*scale, h_canvas*scale)

tk.Label(text='评分属性：').place(x=0.33*w_win, y=0.025*h_win, anchor='w')
cmb = ttk.Combobox(window)
cmb.place(x=0.37*w_win, y=0.025*h_win, anchor='w')
# 设置下拉菜单中的值
cmb['value'] = ('noise','detail','expor','color')

changeb = tk.Button(window, text='启用框选打分',  command=changemode)
changeb.place(x=0.25*w_win, y=0.025*h_win, anchor='w')


tk.Label(text='1',bg='green',font=('Arial', 25)).place(x=0.0*w_win, y=0.94*h_win, anchor='w')
var1 = tk.DoubleVar()  
var1.set(2.5) 
#mark1 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var1 ,length = 300,showvalue=1,tickinterval=0.5)
mark1 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var1 ,length = 300,showvalue=0,tickinterval=0.5)
mark1.place(x=0.03*w_win, y=0.94*h_win, anchor='w')

tk.Label(text='2',bg='green',font=('Arial', 25)).place(x=0.25*w_win, y=0.94*h_win, anchor='w')
var2 = tk.DoubleVar()
var2.set(2.5) 
mark2 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var2,length = 300,showvalue=0,tickinterval=0.5)
mark2.place(x=0.27*w_win, y=0.94*h_win, anchor='w')

tk.Label(text='3',bg='green',font=('Arial', 25)).place(x=0.5*w_win, y=0.94*h_win, anchor='w')
var3 = tk.DoubleVar()  
var3.set(2.5) 
mark3 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var3,length = 300,showvalue=0,tickinterval=0.5)
mark3.place(x=0.53*w_win, y=0.94*h_win, anchor='w')

tk.Label(text='4',bg='green',font=('Arial', 25)).place(x=0.75*w_win, y=0.94*h_win, anchor='w')
var4 = tk.DoubleVar() 
var4.set(2.5) 
mark4 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var4,length = 300,showvalue=0,tickinterval=0.5)
mark4.place(x=0.78*w_win, y=0.94*h_win, anchor='w')

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

image_file1 = create(img_open1,box)
image_file2 = create(img_open2,box2)
image_file3 = create(img_open3,box3)
image_file4 = create(img_open4,box4)

canvas1 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image1 = canvas1.create_image(w_canvas, h_canvas, anchor='se',image=image_file1)  
canvas1.place(x=0.5*w_win, y=0.48*h_win, anchor='se')

canvas2 = tk.Canvas(window,height=h_canvas, width=w_canvas)
image2 = canvas2.create_image(0, h_canvas, anchor='sw',image=image_file2)     
canvas2.place(x=0.5*w_win, y=0.48*h_win, anchor='sw')

canvas3 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image3 = canvas3.create_image(w_canvas, 0, anchor='ne',image=image_file3)     
canvas3.place(x=0.5*w_win, y=0.48*h_win, anchor='ne')

canvas4 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image4 = canvas4.create_image(0, 0, anchor='nw',image=image_file4)  
canvas4.place(x=0.5*w_win, y=0.48*h_win, anchor='nw')

rect1 = canvas1.create_rectangle(0, 0, 1, 1)
rect2 = canvas2.create_rectangle(0, 0, 1, 1)
rect3 = canvas3.create_rectangle(0, 0, 1, 1)
rect4 = canvas4.create_rectangle(0, 0, 1, 1)
canvas1.delete(rect1)
canvas2.delete(rect2)
canvas3.delete(rect3)
canvas4.delete(rect4)


b = tk.Button(window, text='上传打分(ctrl+u)', font=('Arial', 12), command=upload)
b.place(x=0.61*w_win, y=0.025*h_win, anchor='w')

b0= tk.Button(window, text='对齐(ctrl+m)', font=('Arial', 12),command=update)
b0.place(x=0.51*w_win, y=0.025*h_win, anchor='w')
#b0.bind('<Control-Key-m>')

b3= tk.Button(window, text='上一组(crtl+ ← )', font=('Arial', 12),command=previous)
b3.place(x=0.71*w_win, y=0.025*h_win, anchor='w')

b2= tk.Button(window, text='下一组(crtl+ → )', font=('Arial', 12),command=next)
b2.place(x=0.81*w_win, y=0.025*h_win, anchor='w')

b1= tk.Button(window, text='保存(ctrl+s)', font=('Arial', 12),command=save)
b1.place(x=0.91*w_win, y=0.025*h_win, anchor='w')

# insimgopen = Image.open('ins.png')
# region = insimgopen.resize((int(w_win*0.1), int(h_win*0.35)))
# insimagefile = ImageTk.PhotoImage(image = region)
# Lab= tk.Label(window,image= insimagefile)
# Lab.place(x=0.85*w_win, y=0.75*h_win, anchor='w')


window.bind("<MouseWheel>",scaler)
window.bind("<B1-Motion>",drag)
window.bind("<ButtonRelease-1>",locclear)
window.bind('<Control-Key-m>',update_key)
window.bind('<Control-Key-u>',upload_key)
window.bind('<Control-Key-s>',save_key)
window.bind('<Double-Button-1>',display)
window.bind('<Control-Right>',next_key)
window.bind('<Control-Left>',previous_key)


#window.attributes("-topmost",True)
window.mainloop()