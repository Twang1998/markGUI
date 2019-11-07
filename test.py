import csv

sv_file=csv.reader(open('D:\\Bishe\\DataSet\\dataset\\052/052Noise.csv','r',encoding='ANSI'))
content = []
for line in sv_file:
    content.append([line[2],line[6]])

print(content)