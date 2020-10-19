#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil

def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    imgpath = os.path.join(path, "image")
    xmlpath = os.path.join(path, "xml")
    imglist = os.listdir(imgpath)
    xmllist = os.listdir(xmlpath)
    # print f_list
    print(len(imglist))
    print(len(xmllist))
    a = []
    b = []
    c = []
    for i in imglist:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.jpg':
            a.append(os.path.splitext(i)[0])
            #print(a)
    print(len(a))
    for i in xmllist:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.xml':
            #print(os.path.splitext(i)[0])
            b.append(os.path.splitext(i)[0])
        elif os.path.splitext(i)[1] != '.xml':
            rpath = os.path.join(xmlpath, i)
            os.remove(rpath)
    print(len(b))
    for k in a:
        if k not in b:
            #print(k)
            filename = str(k) + ".jpg"
            print(filename)
            revdir = os.path.join(imgpath, filename)
            os.remove(revdir)
            c.append(k)
    print(len(c))
    for m in b:
        if m not in a:
            print(m)
            fname = str(m)+".xml"
            rdir = os.path.join(xmlpath,fname)
            os.remove(rdir)
if __name__ == '__main__':
    path = '/home/nie/nmh/AABB'
    getFileName(path)