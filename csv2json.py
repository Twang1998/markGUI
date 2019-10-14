# -*- coding: utf-8 -*-
"""
Spyder Editor
"D:\\opentest\\2.jpg"
This is a temporary script file.
"""
#import csv
#filename = 'D:/新建文件夹/大数据挖掘/QA/train.csv'
#with open(filename,'r'，encoding=“utf-8”) as f:
#    reader = csv.reader(f)
#    rows = [row for row in reader]
#    print(list(reader))
#    print(reader[1])


#import csv
#with open('D:/新建文件夹/大数据挖掘/QA/train.csv','r'，encoding=“utf-8”) as csvfile:
#    reader = csv.reader(csvfile)
#    rows = [row for row in reader]
#str_1='wo shi yi zhi da da niu '
#char_1='shi yi'
#nPos=str_1.index(char_1)
#print(nPos)

import json
import csv
import pandas as pd
 
# Python 字典类型转换为 JSON 对象
#a="dsfdfs"
#data = {
#    'no' : 1,
#    'name' : a,
#    'url' : 'http://www.runoob.com'
#}
# 
#json_str = json.dumps(data)
#print ("Python 原始数据：", repr(data))
#print ("JSON 对象：", json_str)
csvfile=open('D:/新建文件夹/大数据挖掘/QA/train.csv','r',encoding='UTF-8')
#names=("Question","Abs","Answer")
#reader=csv.DictReader(csvfile)
#for row in reader:
#    print (row['Question'])
df = pd.read_csv("D:/新建文件夹/大数据挖掘/QA/train.csv",nrows=11470,usecols=['Question','Abs','Answer'])
dff=df
#dff=df.loc[25:100]
#for row in df.index:
#    print (df.loc[row].Question)
jsonfile=open('D:/a.json','w')

#id = 0
#context = "cshsfkfhdksfhkasjdesklhcfksdjfhsdjkfhds"
#text = "cf"
#n=context.index(text)
#question = "sddsfddf"
data=[]
i=1
for row in dff.index:
    print (dff.loc[row].Question)
    idx = dff.loc[row].Question
    context = dff.loc[row].Abs
    text = dff.loc[row].Answer
    n=context.index(text)
    if idx=='A1':
        question = "What is the objective or aim of this paper?"+idx
    elif idx=='A2':
        question = "What problem(s) does this paper address?"+idx
    elif idx=='A41':
        question = " What method or approach does this paper propose?"+idx
    elif idx=='A51':
        question = "What is this method based on?"+idx
    elif idx=='A61':
        question = "How does the proposed method differ from previous methods or approaches?"+idx
    elif idx=='A42':
        question = "What model does this paper propose?"+idx
    elif idx=='A52':
        question = "What is this model based on?"+idx
    elif idx=='A62':
        question = "How does the proposed model differ from previous models?"+idx
    elif idx=='A43':
        question = "What algorithm does this paper propose?"+idx
    elif idx=='A53':
        question = "What is this algorithm based on?"+idx
    elif idx=='A63':
        question = " How does the proposed algorithm differ from previous algorithms?"+idx
    elif idx=='A44':
        question = " What framework does this paper propose?"+idx
    elif idx=='A54':
        question = " What is this framework based on?"+idx
    elif idx=='A64':
        question = "How does the proposed framework differ from previous frameworks?"+idx
    elif idx=='A45':
        question = "What datasetdoes this paper propose?"+idx
    elif idx=='A7':
        question = " What experiment does this paper carry out to evaluate the result?"+idx
    elif idx=='A81':
        question = "What does the result of this paper show(demonstrated by the experiment)?"+idx
    elif idx=='A82':
        question = "What does the result of this paper show(demonstrated by the experiment)?"+idx
    elif idx=='A83':
        question = "What does the result of this paper show(demonstrated by the experiment)?"+idx
    elif idx=='A10':
        question = " How does this result outperform existing work?"+idx
    else:
        question = "How does this result outperform existing work?"+idx
    answers=[]
    d=dict()
    d['text'] = text
    d['answer_start'] = n
    answers.append(d)
#    d.clear()
    
    qas=[]
    e=dict()
    e['id']=i
    i=i+1
    e['question']=question
    e['answers']=answers
    qas.append(e)
#    e.clear()
    
    paragraphs=[]
    f=dict()
    f['context']=context
    f['qas']=qas
    paragraphs.append(f)
#    f.clear()
    

    g=dict()
    g['title']=" "
    g['paragraphs']=paragraphs    
    data.append(g)
#    g.clear()
    
h=dict()
h['data']=data
h['version']="1.1"
json.dump(h,jsonfile)



