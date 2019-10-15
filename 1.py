
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

window = tk.Tk()
 



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

def selectPath():
    global pathh
    global path
    global image_file1,image_file2,image_file3,image_file4
    global img1,img2,img3,img4
    global filesname
    global img_open1,img_open2,img_open3,img_open4
    global box,box2,box3,box4,scale
    global w_canvas,h_canvas,maxscale
    global group
    scale =maxscale
    box = (0, 0, w_canvas*scale, h_canvas*scale)    
    box2 = box
    box3 = box
    box4 = box
    path = tkinter.filedialog.askdirectory()
    pathh.set(path)

    filesname = getfilesname(path)

    while(len(filesname) == 0 or len(filesname)%4 != 0):
        path = tkinter.filedialog.askdirectory()
        pathh.set(path)
        filesname = getfilesname(path)
    group += 1
    img1 = cv2.imread(filesname[0],0)
    img2 = cv2.imread(filesname[1],0)
    img3 = cv2.imread(filesname[2],0)
    img4 = cv2.imread(filesname[3],0)
    
    img_open1 = Image.open(filesname[0])
    img_open2 = Image.open(filesname[1])
    img_open3 = Image.open(filesname[2])
    img_open4 = Image.open(filesname[3])

    image_file1 = create(img_open1,box)
    image_file2 = create(img_open2,box2)
    image_file3 = create(img_open3,box3)
    image_file4 = create(img_open4,box4)

    putimage()

def print_selection():
    print('you have selected ' + var.get())

def create(img_open,box):
    global w_canvas,h_canvas
    region = img_open.crop(box)     

    region1 = region.resize((w_canvas, h_canvas))

    image_file = ImageTk.PhotoImage(image = region1)
    return image_file

def putimage():
    global canvas1,canvas2,canvas3,canvas4
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



def hit_me():
    global var1,var2,var3,var4
    global box,box2,box3,box4
    global filesname
    global group
    global data
    c = [box,box2,box3,box4]
    d = [var1.get(),var2.get(),var3.get(),var4.get()]
    idbegin = 4*group-3
    for i in range(4):
        b = []
        b.append(idbegin + i)
        b.append(filesname[i])
        b.append(c[i])
        b.append(cmb.get())
        b.append(d[i])
        data.append(b)
    print(data)


    

def finish():
    #global path
    global data
    data = sorted(data)
    jsonfile=open(os.getcwd()+'/a.json','w')
    dataa = []
    for i in range(len(data)):
        id = data[i][0]
        path = data[i][1]
        area = data[i][2]
        attribute = data[i][3]
        score = data[i][4]

        content = []
        a = dict()
        a['area'] = area
        a['attribute'] = attribute
        a['score'] = score
        content.append(a)

        h = dict()
        h['id'] = id
        h['path'] = path
        h['content'] = content
        dataa.append(h)
    d=dict()
    d['data']=dataa 
    json.dump(d,jsonfile)

    
    name_attribute = ['id','path','area','arrtibute','score']
    csvFile = open(os.getcwd()+'./a.csv', "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow(name_attribute)
    for i in range(len(data)):
        writer.writerow(data[i])
   

def drag(event):
    global box,box2,box3,box4
    global img1,img2,img3,img4
    global image_file1,image_file2,image_file3,image_file4
    global loc
    global scale
    global w_canvas,h_canvas,maxscale
    nowloc=[]
    if (event.widget == canvas1 or event.widget == canvas2 or event.widget == canvas3 or event.widget == canvas4):

        nowloc.append(event.x)
        nowloc.append(event.y)
        loc.append(nowloc)
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


def scaler(event):
    global scale
    global box,box2,box3,box4
    global img1,img2,img3,img4
    global image_file1,image_file2,image_file3,image_file4
    global w_canvas,h_canvas,maxscale,w_win,h_win
    
    # print(event.x_root,event.y_root,event.widget,event.type)
    # print(event.widget == canvas1)
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

def locclear(event):
    global loc
    loc.clear()

def match(img1,img2,box1):
    img = img2
    print(img1)
    print(box1)
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



window.title('My Window')

w_win = window.winfo_screenwidth()
h_win = window.winfo_screenheight()

big = str(w_win) + 'x' + str(h_win)
window.geometry(big) 

w_canvas =int(w_win*0.4)
h_canvas = int(h_win*0.4)

group = 1
data = []
#path = 'C:/Users/37151/Desktop/tkinter/sense1'
path = os.getcwd() + '/sense1'
path=path.replace("\\","/")
print(path)
pathh = tk.StringVar()
tk.Label(window,text = "目标路径:").place(x=0.2*w_win, y=0.025*h_win, anchor='w')
tk.Entry(window, textvariable = pathh).place(x=0.3*w_win, y=0.025*h_win,width = 300, anchor='w')
tk.Button(window, text = "路径选择", command = selectPath).place(x=0.6*w_win, y=0.025*h_win, anchor='w')

filesname=getfilesname(path)
print(filesname[0])

img1 = cv2.imread(filesname[0],0)
img2 = cv2.imread(filesname[1],0)
img3 = cv2.imread(filesname[2],0)
img4 = cv2.imread(filesname[3],0)

img_open1 = Image.open(filesname[0])
img_open2 = Image.open(filesname[1])
img_open3 = Image.open(filesname[2])
img_open4 = Image.open(filesname[3])

w_img = img_open1.size[0]
h_img = img_open1.size[1]

maxscale = min(int(w_img/w_canvas),int(h_img/h_canvas))

scale = maxscale

loc = []

box = (0, 0, w_canvas*scale, h_canvas*scale)  
box2 = (0, 0, w_canvas*scale, h_canvas*scale)
box3 = (0, 0, w_canvas*scale, h_canvas*scale)
box4 = (0, 0, w_canvas*scale, h_canvas*scale)

tk.Label(text='评分属性(请下拉选择)：').place(x=0.85*w_win, y=0.15*h_win, anchor='w')
cmb = ttk.Combobox(window)
cmb.place(x=0.85*w_win, y=0.2*h_win, anchor='w')
# 设置下拉菜单中的值
cmb['value'] = ('noise','detail','expor','color')

var1 = tk.StringVar()   
#mark1 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var1 ,length = 300,showvalue=1,tickinterval=0.5)
mark1 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var1 ,length = 400,showvalue=0,tickinterval=0.5)
mark1.place(x=0.1*w_win, y=0.075*h_win, anchor='w')

var2 = tk.StringVar()
mark2 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var2,length = 400,showvalue=0,tickinterval=0.5)
mark2.place(x=0.5*w_win, y=0.075*h_win, anchor='w')

var3 = tk.StringVar()  
mark3 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var3,length = 400,showvalue=0,tickinterval=0.5)
mark3.place(x=0.1*w_win, y=0.925*h_win, anchor='w')

var4 = tk.StringVar() 
mark4 = tk.Scale(window,from_=0,  to=5,  resolution=0.5, orient=tk.HORIZONTAL , variable=var4,length = 400,showvalue=0,tickinterval=0.5)
mark4.place(x=0.5*w_win, y=0.925*h_win, anchor='w')


image_file1 = create(img_open1,box)
image_file2 = create(img_open2,box2)
image_file3 = create(img_open3,box3)
image_file4 = create(img_open4,box4)

canvas1 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image1 = canvas1.create_image(w_canvas, h_canvas, anchor='se',image=image_file1)  
canvas1.place(x=0.4*w_win, y=0.5*h_win, anchor='se')

canvas2 = tk.Canvas(window,height=h_canvas, width=w_canvas)
image2 = canvas2.create_image(0, h_canvas, anchor='sw',image=image_file2)     
canvas2.place(x=0.4*w_win, y=0.5*h_win, anchor='sw')

canvas3 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image3 = canvas3.create_image(w_canvas, 0, anchor='ne',image=image_file3)     
canvas3.place(x=0.4*w_win, y=0.5*h_win, anchor='ne')

canvas4 = tk.Canvas(window, height=h_canvas, width=w_canvas)
image4 = canvas4.create_image(0, 0, anchor='nw',image=image_file4)  
canvas4.place(x=0.4*w_win, y=0.5*h_win, anchor='nw')
  
b = tk.Button(window, text='upload(点一下就行)', font=('Arial', 12), command=hit_me)
b.place(x=0.85*w_win, y=0.45*h_win, anchor='w')

b0= tk.Button(window, text='match', font=('Arial', 12), width = 5,command=update)
b0.place(x=0.85*w_win, y=0.4*h_win, anchor='w')

b1= tk.Button(window, text='finish', font=('Arial', 12), width = 5,command=finish)
b1.place(x=0.85*w_win, y=0.5*h_win, anchor='w')

insimgopen = Image.open('ins.png')
region = insimgopen.resize((int(w_win*0.1), int(h_win*0.35)))
insimagefile = ImageTk.PhotoImage(image = region)
Lab= tk.Label(window,image= insimagefile)
Lab.place(x=0.85*w_win, y=0.75*h_win, anchor='w')


window.bind("<MouseWheel>",scaler)
window.bind("<B1-Motion>",drag)
window.bind("<ButtonRelease-1>",locclear)



window.attributes("-topmost",True)
window.mainloop()