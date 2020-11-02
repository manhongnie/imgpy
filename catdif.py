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
        if os.path.splitext(i)[1] == '.bmp':
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
        if k in b:
            #print(k)
            filename = str(k) + ".bmp"
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

def shanchuFileName(srcpath, dstpath):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    #imgpath = os.path.join(path, "image")
    #xmlpath = os.path.join(path, "xml")
    imglist = os.listdir(srcpath)
    xmllist = os.listdir(dstpath)
    # print f_list
    print(len(imglist))
    print(len(xmllist))
    a = []
    b = []
    c = []
    for i in imglist:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.bmp':
            a.append(os.path.splitext(i)[0])
            #print(a)
    print(len(a))
    for i in xmllist:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.xml':
            #print(os.path.splitext(i)[0])
            b.append(os.path.splitext(i)[0])
        elif os.path.splitext(i)[1] != '.xml':
            rpath = os.path.join(dstpath, i)
            os.remove(rpath)
    print(len(b))
    for k in a:
        if k in b:
            #print(k)
            filename = str(k) + ".bmp"
            print(filename)
            revdir = os.path.join(srcpath, filename)
            os.remove(revdir)
            c.append(k)
    print(len(c))
    # for m in b:
    #     if m not in a:
    #         print(m)
    #         fname = str(m)+".bmp"
    #         rdir = os.path.join(dstpath, fname)
    #         os.remove(rdir)

if __name__ == '__main__':
    path = 'D:/jinkeloc/train'
    srcpath = "D:/jinkeloc/train/timg"
    dstpath = "D:/jinkeloc/train/xml"
    #getFileName(path)
    shanchuFileName(srcpath, dstpath)