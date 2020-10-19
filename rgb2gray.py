#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import cv2

def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    imgpath = os.path.join(path, "lagerimg")
    dstpath = os.path.join(path, "grayimg")
    f_list = os.listdir(imgpath)
    # print f_list
    print(len(f_list))
    #os.path.isdir(path)
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    a = []
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.bmp':
            #print(os.path.splitext(i)[0])
            a.append(i)
    print(len(a))
    for k in range(len(a)):
        imgfile = os.path.join(imgpath, a[k])
        img = cv2.imread(imgfile)
        b, g, r = cv2.split(img)
        dst = cv2.merge([g, g, g])
        #print(dst)
        dstfile = os.path.join(dstpath, a[k])
        #print(dst.shape)
        cv2.imwrite(dstfile, dst)

if __name__ == '__main__':
    path = '/home/nie'
    #dstpath = "/media/nie/9E6052E56052C425/jufei3030caisepjie/imggray"
    getFileName(path)


