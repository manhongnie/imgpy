import os
import shutil
import sys
from datetime import datetime
import cv2

def huiduhua(filepath,w,h):
    fileNames = os.listdir(filepath)
    for file in fileNames:
        if os.path.splitext(file)[1] == '.bmp':
            img = cv2.imread(os.path.join(filepath, file))
            imgsize = cv2.resize(img, (w, h))
            (b, g, r) = cv2.split(imgsize)
            cv2.imwrite(os.path.join(filepath, file), imgsize)

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
            shutil.copyfile(os.path.join(srcpath, file), os.path.join(dstpath, file))
if __name__ == "__main__":
    filepath = "D:/jinkeloc/jklabel"
    dstpath = "/home/nie/nmh/GppTest/Testimg"
    w = 330
    h = 350
    huiduhua(filepath,w,h)
    #modFile(filepath)
    #copyfile(filepath, dstpath)

