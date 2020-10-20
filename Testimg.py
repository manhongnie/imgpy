import os
import shutil
import sys
from datetime import datetime
import cv2
import numpy as np

def testimg(srcfile):
    img = cv2.imread(srcfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    contours, hiera = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, countour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(countour)
        if w / h > 0.5 and w / h < 1.5 and w > 220 and h > 220 and w < 480 and h < 480:
            print(x, "  ", y, "  ", x+w, "  ", y+h)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3, 8, 1)

    cv2.imshow("zhanshi", img)
    cv2.waitKey(0)
    cv2.destroyWindow("zhanshi")

if __name__ == '__main__':
    srcfile = "/home/nie/nmh/jinkeimg1019/5404.bmp"
    testimg(srcfile)