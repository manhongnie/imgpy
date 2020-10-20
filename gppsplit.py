
import os
import shutil
import sys
from datetime import datetime
import cv2

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
    litww = 200
    lithh = 200
    ww = 200
    hh = 200
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
            if w/h > 0.5 and w/h < 1.5 and w > litww and h > lithh and w < 520 and h < 520:
                savefile = savepath + "/" + str(i) + ".bmp"
                #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2, 8)
                saveimg = img[int(y): int(y + h), int(x): int(x + w)]
                #print("baocunde lujing : ", savefile)
                cv2.imwrite(savefile, saveimg)

def modFile(filepath):
    # 获取当前路径下的文件名，返回List
    fileNames = os.listdir(filepath)
    dtime = datetime.now()
    for file in fileNames:
        if os.path.splitext(file)[1] == '.bmp':
            os.rename(os.path.join(filepath, file), os.path.join(filepath, dtime.strftime('%Y%m%d%H%M%S%f') + file))
def copyfile(srcpath, dstpath):
    fileNames = os.listdir(srcpath)
    isExistsk = os.path.exists(srcpath)
    if not isExistsk:
        # 如果不存在则创建目录
        print(srcpath+' non-existent')
        sys.exit(0)
    isExists = os.path.exists(dstpath)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(dstpath)
        print(dstpath+' 目录创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(dstpath+' 目录已存在')
    for file in fileNames:
        if os.path.splitext(file)[1] == '.bmp':
            #shutil.copyfile(os.path.join(srcpath, file), os.path.join(dstpath, file))
            srcfile = os.path.join(srcpath, file)
            img = cv2.imread(srcfile)
            b, g, r = cv2.split(img)
            gray = cv2.subtract(r, g)
            #dst = cv2.GaussianBlur(img, (3, 3), 0)
            #gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
            #cv2.imshow("111", binary)
            #cv2.waitKey(0)
            contours, hiera = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for i, countour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(countour)
                area = cv2.contourArea(countour)
                if area > (binary.shape[0] * binary.shape[1]) / 5:
                    print("kai shi cai tu !")
                    saveimg = img[int(y - 20): int(y + h + 20), int(x - 20): int(x + w + 20)]
                    cv2.imwrite(os.path.join(dstpath, file), saveimg)

def shantu(dstpath):
    fileNames = os.listdir(dstpath)
    for file in fileNames:
        if os.path.splitext(file)[1] == '.bmp':
            dstfile = os.path.join(dstpath, file)
            try:
                img = cv2.imread(dstfile)
                if img.shape[0] < 300 or img.shape[1] < 300:
                    os.remove(dstfile)
            except:
                os.remove(dstfile)
if __name__ == '__main__':
    path = "D:/jinkeimg/1014xie"
    #print("裁剪文件夹！")
    #src_root = input()
    #aimg = zhaotu(path)
    #bimg = zhaolujing(path)
    #spimg(path, aimg, bimg)
    srcpath = "D:/jinkeimg/1014xie/10"
    dstpath = "D:/jinkeimg/1014xie/timg"
    #modFile(srcpath)
    #copyfile(srcpath, dstpath)
    shantu(dstpath)