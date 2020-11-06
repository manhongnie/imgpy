import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QFileDialog,
                             QTextEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication
import sys
from PyQt5.QtWidgets import QMessageBox
import xml.dom.minidom



class splitimg(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.a = chaitu()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('这是一个 <b>处理标注数据</b> 脚本')
        self.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")


        #folder_name = QFileDialog.getExistingDirectory(self, '标题', './')  # 可设置默认路径

        btn = QPushButton('exit', self)
        btn.setToolTip('这是一个 <b>退出</b> 按钮')
        # default size
        btn.resize(100, 100)
        btn.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        btn.move(1050, 650)
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 1200, 800)
        self.center()
        src = QPushButton('open xml file', self)
        src.resize(300, 100)
        src.move(50, 50)
        src.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        src.clicked.connect(self.srcopenimg)
        #luj = QtWidgets.QLineEdit(self)

        runimg = QPushButton('Process the xml file', self)
        runimg.resize(300, 100)
        runimg.move(450, 50)
        runimg.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")

        runimg.clicked.connect(self.initimg)
        self.text_edit = QTextEdit(self)
        self.text_edit.resize(950, 350)
        self.text_edit.move(50, 400)
        self.text_edit.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        #text = text_edit.toPlainText()
        runxml = QPushButton('Show label category', self)
        runxml.resize(300, 100)
        runxml.move(850, 50)
        runxml.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")

        runxml.clicked.connect(self.initlabel)

        imgbtn = QPushButton('open the image path', self)
        imgbtn.resize(300, 100)
        imgbtn.move(50, 250)
        imgbtn.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        imgbtn.clicked.connect(self.imgopen)

        xmlbtn = QPushButton('open the xml path', self)
        xmlbtn.resize(300, 100)
        xmlbtn.move(450, 250)
        xmlbtn.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        xmlbtn.clicked.connect(self.xmlopen)

        shanbtn = QPushButton('Process img or xml', self)
        shanbtn.resize(300, 100)
        shanbtn.move(850, 250)
        shanbtn.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")
        shanbtn.clicked.connect(self.initshan)

        self.setWindowTitle('Process xml')
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
        global xmlpath
        xmlpath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "D:\\")

    def imgopen(self):
        global imgdir
        imgdir = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "D:\\")

    def xmlopen(self):
        global xmldir
        xmldir = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "D:\\")

    def initimg(self):
        self.changexml(xmlpath)
        self.text_edit.append("Your xml file has been processed !!!")

    def initlabel(self):
        self.xmlname(xmlpath)

    def initshan(self):
        self.getFileName(imgdir, xmldir)
        self.text_edit.append("Your pictures and annotation files have been processed !!!")

    def changexml(self, xmlpath):
        #global s
        xmllist = os.listdir(xmlpath)
        for c in xmllist:
            if os.path.splitext(c)[1] == '.xml':
                doc = ET.parse(os.path.join(xmlpath, c))
                root = doc.getroot()
                s = root.findall('object')
                if not s:
                    os.remove(os.path.join(xmlpath, c))

    def xmlname(self, xmlpath):
        xlist = os.listdir(xmlpath)  # 列出文件夹下所有的目录与文件
        ## 空列表
        classes_list = []
        num = []
        for i in range(0, len(xlist)):
            path = os.path.join(xmlpath, xlist[i])
            if os.path.isfile(path):
                # 打开xml文档
                dom = xml.dom.minidom.parse(path)

                # 得到文档元素对象
                root = dom.documentElement
                cc = dom.getElementsByTagName('name')
                # print("cc :  ",cc)

                for i in range(len(cc)):
                    c1 = cc[i]
                    # print("c1 :  ",c1)
                    # 列表中不存在则存入列表
                    if classes_list.count(c1.firstChild.data) == 0:
                        # print("c1.firstChild.data :  ",type(c1.firstChild.data))
                        classes_list.append(c1.firstChild.data)
        for k in range(len(classes_list)):
            num.append(0)
        for i in range(0, len(xlist)):
            path = os.path.join(xmlpath, xlist[i])
            if os.path.isfile(path):
                # 打开xml文档
                dom = xml.dom.minidom.parse(path)
                # 得到文档元素对象
                root = dom.documentElement
                cc = dom.getElementsByTagName('name')
                # print("cc :  ",cc)
                for i in range(len(cc)):
                    c1 = cc[i]
                    for j in range(len(classes_list)):
                        if c1.firstChild.data == classes_list[j]:
                            num[j] = num[j] + 1

        self.text_edit.append(str(classes_list))
        self.text_edit.append("label num :  " + str(len(classes_list)))
        for i in range(len(classes_list)):
            #print(classes_list[i], " :  ", num[i])
            self.text_edit.append(str(classes_list[i]) + " :  " + str(num[i]))

    def getFileName(self, imgdir, xmldir):

        imglist = os.listdir(imgdir)
        xmllist = os.listdir(xmldir)
        # print f_list
        #print(len(imglist))
        #print(len(xmllist))
        a = []
        b = []
        c = []
        d = []
        for i in imglist:
            if os.path.splitext(i)[1] in ['.bmp', '.jpg', '.png', '.tif']:
                a.append(os.path.splitext(i)[0])
                if i.endswith('.bmp'):
                    d.append('.bmp')
                if i.endswith('.jpg'):
                    d.append('.jpg')
                if i.endswith('.png'):
                    d.append('.png')
                if i.endswith('.tif'):
                    d.append('.tif')
                # print(a)
        #print(len(a))
        for i in xmllist:
            if os.path.splitext(i)[1] == '.xml':
                # print(os.path.splitext(i)[0])
                b.append(os.path.splitext(i)[0])
            elif os.path.splitext(i)[1] != '.xml':
                rpath = os.path.join(xmldir, i)
                os.remove(rpath)
        #print(len(b))
        for k in a:
            if k not in b:
                # print(k)
                nm = a.index(k)
                filename = str(k) + str(d[nm])
                print(filename)
                revdir = os.path.join(imgdir, filename)
                os.remove(revdir)
                c.append(k)
        print(len(c))
        for m in b:
            if m not in a:
                #print(m)
                fname = str(m) + ".xml"
                rdir = os.path.join(xmldir, fname)
                os.remove(rdir)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = splitimg()
    sys.exit(app.exec_())