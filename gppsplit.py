
import cv2
import os
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt

def zhaotu(path):
    imagelist = os.listdir(path)
    aimg = []
    for i in imagelist:
        if os.path.splitext(i)[1] == '.tif':
            aimg.append(i)
            #print(aimg[0])
    return aimg

def zhaolujing(path):
    imglist = os.listdir(path)
    bimg = []
    for k in imglist:
        if os.path.splitext(k)[1] == ".tif":
            bimg.append(os.path.splitext(k)[0])
    for c in range(len(bimg)):
        print(bimg[c])
    return bimg
def spimg(path, aimg, bimg):
    #ap = []
    litww = 320
    lithh = 320
    ww = 250
    hh = 250
    for ik in range(len(aimg)):
        srcfile = os.path.join(path, aimg[ik])
        print(srcfile)
        img = cv2.imread(srcfile)
        dst =cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray,0,255,cv2.THRESH_OTSU | cv2.THRESH_BINARY)
        contours, hiera = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if not os.path.exists(os.path.join(path, bimg[ik])):
            os.makedirs(os.path.join(path, bimg[ik]))
        savepath = os.path.join(path, bimg[ik])
        for i, countour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(countour)
            if w/h > 0.5 and w/h < 1.5 and w > litww and h > lithh and w < 380 and h < 380:
                savefile = savepath + "/" + str(i) + ".bmp"
                #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2, 8)
                saveimg = img[int(y): int(y + h), int(x): int(x + w)]
                print("baocunde lujing : ", savefile)
                cv2.imwrite(savefile, saveimg)
if __name__ == '__main__':
    path = "D:\\jinkeimg\\1014xie"
    #print("裁剪文件夹！")
    #src_root = input()
    aimg = zhaotu(path)
    bimg = zhaolujing(path)
    spimg(path, aimg, bimg)