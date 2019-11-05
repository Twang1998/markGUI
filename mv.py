# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:14:20 2019

@author: lenovo
"""



import shutil,os

srcpath = "C:\\Users\\37151\\Desktop\\U11"
dstpath = "D:\\Bishe\\DataSet\\HuaWei"


# i = 1
# for filename in os.listdir(srcpath):
#     print (filename)
#     for picname in os.listdir(srcpath+'/'+filename):
#         print (picname)
#         #shutil.move(srcpath+'/'+filename+'/'+picname,srcpath+'/'+filename+'/'+filename[0]+'_'+str(i)+'.jpg')
#         senseid = "%03d"%i
#         if(not os.path.exists(dstpath+'/'+senseid) ):
#             os.mkdir(dstpath+'/'+senseid)
#         shutil.copy(srcpath+'/'+filename+'/'+picname,dstpath+'/'+senseid+'/')
#         i += 1
#     i=1

# 加入 M,N,O
i = 1
for picname in os.listdir(srcpath):
    print (picname)
    #shutil.move(srcpath+'/'+filename+'/'+picname,srcpath+'/'+filename+'/'+filename[0]+'_'+str(i)+'.jpg')
    senseid = "%03d"%i
    if(not os.path.exists(dstpath+'/'+senseid) ):
        os.mkdir(dstpath+'/'+senseid)
    shutil.copy(srcpath+'/'+picname,dstpath+'/'+senseid+'/')
    i += 1

#rename 一个文件夹
# p = 'C:\\Users\\37151\\Desktop/U11'
# for picname in os.listdir(p):
#     print (picname)
#     a = (picname[3:-5])
#     if(len(a) == 1):
#         a = '00'+a
#     if(len(a) == 2):
#         a = '0'+a
#     # print(a)
#     # if(len(picname)<9):
#     shutil.move(p+'/'+picname,p+'/'+picname[0]+'_'+a+'.jpg')

#rename 15个文件夹
# srcpath = "C:\\Users\\37151\\Desktop\\phone"
# i = 139
# for filename in os.listdir(srcpath):
#     for picname in os.listdir(srcpath+'/'+filename):
#         print (picname)
#         senseid = "%03d"%i

#         # print(a)
#         # if(len(picname)<9):
#         shutil.move(srcpath+'/'+filename+'/'+picname,srcpath+'/'+filename+'/'+filename[0]+'_'+senseid+'.jpg')
#         i += 1
#     i = 139

#终极重命名+分配  要求：1.确保每个手机文件夹下顺序一致；2.修改手机文件夹的名字——加前缀ABCDEFG.....
i = 139
for filename in os.listdir(srcpath):
    print (filename)
    for picname in os.listdir(srcpath+'/'+filename):
        print (picname)
        senseid = "%03d"%i
        shutil.move(srcpath+'/'+filename+'/'+picname,srcpath+'/'+filename+'/'+filename[0]+'_'+senseid+'.jpg')
        
        if(not os.path.exists(dstpath+'/'+senseid) ):
            os.mkdir(dstpath+'/'+senseid)
        shutil.copy(srcpath+'/'+filename+'/'+filename[0]+'_'+senseid+'.jpg',dstpath+'/'+senseid+'/')
        i += 1
    i=139