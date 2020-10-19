import os
import cv2

def getFileName(imgpath):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    imglist = os.listdir(imgpath)
    for i in imglist:
        if os.path.splitext(i)[1] == '.jpg':
            srcflie = os.path.join(imgpath, i)
            img = cv2.imread(srcflie)
            filename = os.path.splitext(i)[0] + ".bmp"
            dstfile = os.path.join(imgpath, filename)
            cv2.imwrite(dstfile, img)
            os.remove(srcflie)

if __name__ == '__main__':
    imgpath = '/home/nie/nmh/1'
    getFileName(imgpath)