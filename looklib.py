#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
def copyfile(srcpath,dstpath):
    f_list = os.listdir(path)
    b = []
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.so':
            b.append(i)
    for im in range(len(b)):
        shutil.copyfile(srcpath+"/"+b[im], dstpath+"/"+b[im])

def getFileName(path,txtpath):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    f_list = os.listdir(path)
    # print f_list
    print(len(f_list))
    if not os.path.dirname(txtpath):
        os.makedirs(os.path.dirname(txtpath))
    a = []
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.so':
            #print(os.path.splitext(i)[0])
            c = os.path.splitext(i)[0]
            ac = "\"l\"" + "," + "\"%s\""%c[3:] + ","
            a.append(ac)
    print(len(a))
    txtfile = open(txtpath, 'w') #'D:/opencv420/Releaselib.txt'
    for ik in range(len(a)):
        txtfile.write(a[ik] + '\n')


if __name__ == '__main__':
    txtpath = '/home/nie/nmh/ubso.txt'
    path = '/usr/local/lib'
    getFileName(path, txtpath)
    dspath = "home/nie/nmh/ubso"
    copyfile(path, dspath)