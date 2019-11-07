import csv 
def csv_deal(filename1,filename2,filename3,filename4,dpath):
    #read exposure
    csv_file=csv.reader(open(filename1,'r'))
    content1=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
    for line in csv_file:
        content1.append([line[2],line[4],line[6]])
    i=1
    while(i<16):
        start = i
        if(i<15):
            while (content1[i][2] == content1[i+1][2]):
                # print('content[i][2]:'+content[i][2])
                i = i+1
                if(i==15):
                    break      
        i = i+1
        end = i
        rank = (end + start-1) / 2
        for k in range(start,end):
            content1[k][2] = str(rank)
    content1 = content1[1:]
    content1.sort()
    print(content1)
    #read color
    csv_file=csv.reader(open(filename2,'r'))
    content2=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
    for line in csv_file:
        content2.append([line[2],line[4],line[6]])
    i=1
    while(i<16):
        start = i
        if(i<15):
            while (content2[i][2] == content2[i+1][2]):
                # print('content[i][2]:'+content[i][2])
                i = i+1
                if(i==15):
                    break  
        i = i+1
        end = i
        rank = (end + start-1) / 2
        for k in range(start,end):
            content2[k][2] = str(rank)
    content2 = content2[1:]
    content2.sort()
    print(content2)
    #read noise
    csv_file=csv.reader(open(filename3,'r'))
    content3=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
    for line in csv_file:
        content3.append([line[2],line[4],line[6]])
    i=1
    while(i<16):
        start = i
        if(i<15):
            while (content3[i][2] == content3[i+1][2]):
                # print('content[i][2]:'+content[i][2])
                i = i+1
                if(i==15):
                    break  
        i = i+1
        end = i
        rank = (end + start-1) / 2
        for k in range(start,end):
            content3[k][2] = str(rank)
    content3 = content3[1:]
    content3.sort()
    print(content3)
    #read texture
    csv_file=csv.reader(open(filename4,'r'))
    content4=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
    for line in csv_file:
        content4.append([line[2],line[4],line[6]])
    i=1

    while(i<16):
        start = i
        if(i<15):
            print(str(i)+' '+content4[i][2])
            while (content4[i][2] == content4[i+1][2]):
                # print('content[i][2]:'+content[i][2])
                i = i+1
                if(i==15):
                    break  
        i = i+1
        end = i
        rank = (end + start-1) / 2
        for k in range(start,end):
            content4[k][2] = str(rank)
    content4 = content4[1:]
    content4.sort()
    print(content4)
    f_content=[]
    for i in range(15):
        f_content.append([content1[i][0],str(16-float(content1[i][2])),str(16-float(content2[i][2])),str(16-float(content3[i][2])),str(16-float(content4[i][2]))])
    print(f_content)
    
    name_attribute = [' ','Color','Exposure','Noise','Texture']
    csvFile = open(dpath+'/'+filename1[-12]+filename1[-11]+filename1[-10]+'.csv', "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow(name_attribute)
    for i in range(len(f_content)):
        writer.writerow(f_content[i])
    f_content = []
#csv_deal('011Color.csv','011Exposure.csv','011Noise.csv','011Texture.csv')
import shutil,os

srcpath = "C:\\Users\\37151\\Desktop\\deall"
#dstpath = "D:\\Bishe\\DataSet\\HuaWei"


i = 1
for filename in os.listdir(srcpath):
    deal=[]
    for picname in os.listdir(srcpath+'/'+filename):
        if(picname[-1]=='v'):
            deal.append(picname)
    print(deal)
    csv_deal(srcpath+'/'+filename+'/'+deal[0],srcpath+'/'+filename+'/'+deal[1],srcpath+'/'+filename+'/'+deal[2],srcpath+'/'+filename+'/'+deal[3],srcpath+'/'+filename)

        #shutil.move(srcpath+'/'+filename+'/'+picname,srcpath+'/'+filename+'/'+filename[0]+'_'+str(i)+'.jpg')
        # senseid = "%03d"%i
        # if(not os.path.exists(dstpath+'/'+senseid) ):
        #     os.mkdir(dstpath+'/'+senseid)
        # shutil.copy(srcpath+'/'+filename+'/'+picname,dstpath+'/'+senseid+'/')
        # i += 1
    i=1