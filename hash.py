from PIL import Image
import imagehash
import os
path = 'D:\\Bishe\\DataSet\\3\\KiphoneXjpg'

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
filesname = getfilesname(path)


hash = imagehash.phash(Image.open('D:\\Bishe\\DataSet\\3\\BiphoneXSMjpg/B_025.jpg'))
print(hash)
max = 100
string = ''
for i in range(len(filesname)):

    otherhash = imagehash.phash(Image.open(filesname[i]))
    #print(hash - otherhash)
    if(hash-otherhash< max):
        max = hash-otherhash
        string = filesname[i]
print(string)