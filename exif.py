import piexif
import os
path ='C:\\Users\\37151\\Desktop\\t20'

for filename in os.listdir(path):
    print (filename)
    for picname in os.listdir(path+'/'+filename):
       
        piexif.remove(path+'/'+filename+'/'+picname)
#piexif.remove('C:\\Users\\37151\\Desktop\\t20\\013\\D_013.jpg')

#print(path[-9:])