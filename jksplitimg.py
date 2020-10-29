import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QCoreApplication
import sys
from datetime import datetime
import cv2
import time




class splitimg(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.a = chaitu()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('这是一个 <b>QWidget</b> 部件')


        #folder_name = QFileDialog.getExistingDirectory(self, '标题', './')  # 可设置默认路径

        btn = QPushButton('exit', self)
        btn.setToolTip('这是一个 <b>QPushButton</b> 部件')
        # default size
        btn.resize(100, 100)
        btn.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        btn.move(450, 450)
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 600, 600)
        self.center()
        src = QPushButton('open img', self)
        src.resize(200, 100)
        src.move(50, 50)
        src.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        src.clicked.connect(self.srcopenimg)
        #luj = QtWidgets.QLineEdit(self)
        dst = QPushButton('save img', self)
        dst.resize(200, 100)
        dst.move(350, 50)
        dst.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        dst.clicked.connect(self.dstopenimg)
        runimg = QPushButton('run img', self)
        runimg.resize(200, 100)
        runimg.move(200, 200)
        runimg.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")

        runimg.clicked.connect(self.initimg)
        self.setWindowTitle('jkCrop')
        self.setWindowIcon(QIcon('web.jpg'))
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry() # 获得窗口
        cp = QDesktopWidget().availableGeometry().center()# 获得屏幕中心点
        qr.moveCenter(cp)# 显示到屏幕中心
        self.move(qr.topLeft())
    def srcopenimg(self):
        global imgpath
        imgpath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "D:\\")
    def dstopenimg(self):
        global savepath
        savepath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "D:\\")


    def initimg(self):
        print(imgpath)
        print(savepath)
        aimg = self.zhaotu(imgpath)
        #print(aimg)
        bimg = self.zhaolujing(imgpath)
        #print(bimg)
        self.spimg(imgpath, aimg, bimg)
        #print(bimg)
        time.sleep(10)
        self.modFile(imgpath)
        time.sleep(10)
        self.copyfile(imgpath, savepath)
        time.sleep(20)
        self.shantu(savepath)

    def zhaotu(self, path):
        imagelist = os.listdir(path)
        aimg = []
        for i in imagelist:
            if os.path.splitext(i)[1] == '.bmp':
                aimg.append(i)
                # print(aimg[0])
        return aimg

    def zhaolujing(self, path):
        imglist = os.listdir(path)
        bimg = []
        for k in imglist:
            if os.path.splitext(k)[1] == ".bmp":
                bimg.append(os.path.splitext(k)[0])
        #for c in range(len(bimg)):
            #print(bimg[c])
        return bimg

    def spimg(self, path, aimg, bimg):
        # ap = []
        litww = 200
        lithh = 200
        ww = 200
        hh = 200
        for ik in range(len(aimg)):
            srcfile = os.path.join(path, aimg[ik])
            print(srcfile)
            img = cv2.imread(srcfile)
            dst = cv2.GaussianBlur(img, (3, 3), 0)
            gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
            contours, hiera = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if not os.path.exists(os.path.join(path, bimg[ik])):
                os.makedirs(os.path.join(path, bimg[ik]))
            savepath = os.path.join(path, bimg[ik])
            for i, countour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(countour)
                if w / h > 0.5 and w / h < 1.5 and w > litww and h > lithh and w < 520 and h < 520:
                    savefile = savepath + "/" + str(i) + ".bmp"
                    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2, 8)
                    saveimg = img[int(y - 20): int(y + h + 20), int(x - 20): int(x + w + 20)]
                    try:
                        # print("baocunde lujing : ", savefile)
                        cv2.imwrite(savefile, saveimg)
                    except:
                        saveimg = img[int(y): int(y + h), int(x): int(x + w)]
                        cv2.imwrite(savefile, saveimg)

    def modFile(self, filepath):
        # 获取当前路径下的文件名，返回List
        fileNames = os.listdir(filepath)
        for file in fileNames:
            if os.path.isdir(os.path.join(filepath, file)):
                paths = os.path.join(filepath, file)
                files = os.listdir(paths)
                dtime = datetime.now()
                for dfile in files:
                    if os.path.splitext(dfile)[1] == '.bmp':
                        os.rename(os.path.join(paths, dfile),
                                  os.path.join(paths, dtime.strftime('%Y%m%d%H%M%S%f') + dfile))
                        # time.sleep(1)

    def copyfile(self, srcpath, dstpath):
        fileNames = os.listdir(srcpath)
        isExistsk = os.path.exists(srcpath)
        if not isExistsk:
            # 如果不存在则创建目录
            print(srcpath + ' non-existent')
            sys.exit(0)
        isExists = os.path.exists(dstpath)
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(dstpath)
            print(dstpath + ' 目录创建成功')
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(dstpath + ' 目录已存在')

        for file in fileNames:
            if os.path.isdir(os.path.join(srcpath, file)):
                srcs = os.path.join(srcpath, file)
                files = os.listdir(srcs)
                for xfile in files:
                    if os.path.splitext(xfile)[1] == '.bmp':
                        # shutil.copyfile(os.path.join(srcpath, file), os.path.join(dstpath, file))
                        srcfile = os.path.join(srcs, xfile)
                        img = cv2.imread(srcfile)
                        b, g, r = cv2.split(img)
                        gray = cv2.subtract(r, g)
                        # dst = cv2.GaussianBlur(img, (3, 3), 0)
                        # gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
                        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
                        # cv2.imshow("111", binary)
                        # cv2.waitKey(0)
                        contours, hiera = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                        for i, countour in enumerate(contours):
                            x, y, w, h = cv2.boundingRect(countour)
                            area = cv2.contourArea(countour)
                            if area > (binary.shape[0] * binary.shape[1]) / 5:
                                print("Saving image...")
                                try:
                                    saveimg = img[int(y - 20): int(y + h + 20), int(x - 20): int(x + w + 20)]
                                    saveimg = cv2.resize(saveimg, (310, 330))
                                    cv2.imwrite(os.path.join(dstpath, xfile), saveimg)
                                except:
                                    saveimg = img[int(y): int(y + h), int(x): int(x + w)]
                                    saveimg = cv2.resize(saveimg, (310, 330))
                                    cv2.imwrite(os.path.join(dstpath, xfile), saveimg)
        print("Cropping completed !")
    def shantu(self, dstpath):
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

    def zhaowjj(self, path):
        files = os.listdir(path)
        for file in files:
            if os.path.isdir(os.path.join(path, file)):
                print(os.path.join(path, file))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = splitimg()
    sys.exit(app.exec_())