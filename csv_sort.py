import os
import csv

def getfilesname(path):
    filesname = []
    for filename in os.listdir(path):
        #print(os.path.splitext(filename)[0],path[-3:])
        if os.path.splitext(filename)[1] == ".csv" and os.path.splitext(filename)[0] != path[-3:] :
            filesname+=[path+'/'+filename]
    print(filesname)
    return filesname

def rank(alist):
    b= []

    i =0
    while(i<len(alist)):
        tmp = alist[i]
        count = alist.count(tmp)
        for j in range(count):
            test = (i+1+i+count)/2
            b.append(test)
        i += count
    for j in range(15):
        b[j] = 16-b[j]
    return b
def mysort(filesname):

    final = [[]]
    for i in range(4):
        try:
            csv_file=csv.reader(open(filesname[i],'r'))
        
            # print(123)
            # csv_file=csv.reader(open(filesname[i],'r',encoding= 'ANSI'))
            content=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
            name = []
            srcrank = []
            for line in csv_file:
                content.append([line[2],line[6]])
        except:
            csv_file=csv.reader(open(filesname[i],'r',encoding= 'utf-8'))
            content=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
            name = []
            srcrank = []
            for line in csv_file:
                content.append([line[2],line[6]])
        #print(content)
        for j in range(15):  
            srcrank.append(content[j+1][1])
        rerank = rank(srcrank)
        for j in range(15):  
            content[j+1][1] = rerank[j]
        content.sort()
        #print(content)
        if(i ==0):
            final = content
        else:
            for j in range(16):
                final[j].append(content[j][1])
    return final[0:15]

path = 'D:\\Bishe\\DataSet\\dataset'


for filename in os.listdir(path):
    filesname = getfilesname(path+'/'+filename)
    final = mysort(filesname)

    name_attribute = [' ','Color','Exposure','Noise','Texture']
    csvFile = open(path+'/'+filename+'/'+filename+'.csv', "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow(name_attribute)
    for i in range(15):
        writer.writerow(final[i])