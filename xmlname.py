#coding=utf-8
import xml.dom.minidom
import os,sys
 
rootdir = '/home/nie/nmh/AABB/xml'#存有xml的文件夹路径
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
## 空列表
classes_list = []
num = []
for i in range(0,len(list)):
   path = os.path.join(rootdir,list[i])
   if os.path.isfile(path):   
      #打开xml文档
      dom = xml.dom.minidom.parse(path)
 
      #得到文档元素对象
      root = dom.documentElement
      cc=dom.getElementsByTagName('name')
      #print("cc :  ",cc)
              
      for i in range(len(cc)):
         c1 = cc[i]
         #print("c1 :  ",c1)
         #列表中不存在则存入列表
         if classes_list.count(c1.firstChild.data)==0:
            #print("c1.firstChild.data :  ",type(c1.firstChild.data))
            classes_list.append(c1.firstChild.data)
for k in range(len(classes_list)):
   num.append(0)
for i in range(0,len(list)):
   path = os.path.join(rootdir,list[i])
   if os.path.isfile(path):   
      #打开xml文档
      dom = xml.dom.minidom.parse(path)
      #得到文档元素对象
      root = dom.documentElement
      cc=dom.getElementsByTagName('name')
      #print("cc :  ",cc)   
      for i in range(len(cc)):
         c1 = cc[i]
         for j in range(len(classes_list)):
            if c1.firstChild.data == classes_list[j]:
               num[j] = num[j] + 1

print(classes_list)
print(len(classes_list))
for i in range(len(classes_list)):
   print(classes_list[i], " :  ", num[i])
