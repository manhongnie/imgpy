# coding=utf-8
import xml.dom.minidom
import os, sys
import xml.etree.ElementTree as ET

def gaiming(imglist, xmllist, xmlpath, imgpath):
    print("img size : ", len(imglist))
    print("xml size : ", len(xmllist))
    for k in range(0, len(imglist)):
        for i in range(0, len(xmllist)):
            xmldir = os.path.join(xmlpath, xmllist[i])
            if os.path.splitext(imglist[k])[1] == '.bmp' and os.path.splitext(xmllist[i])[1] == '.xml' and os.path.splitext(imglist[k])[0] == os.path.splitext(xmllist[i])[0] and os.path.isfile(xmldir):
                #print(os.path.splitext(imglist[k])[0])
                #imgl=list(os.path.splitext(imglist[k]))
                #xmll = list(os.path.splitext(xmllist[i]))
                #imgl[0] = str(k)
                imgsrc = os.path.join(imgpath, imglist[k])
                imgdst = os.path.join(imgpath, str(k) + '.bmp')
                xmlsrc = os.path.join(xmlpath, xmllist[i])
                xmldst = os.path.join(xmlpath, str(k) + '.xml')
                #print(xmldst)
                os.rename(imgsrc, imgdst)
                os.rename(xmlsrc, xmldst)
def changexml(xmlpath):
    xmllist = os.listdir(xmlpath)
    a = []
    #print(xmllist)
    for c in xmllist:
        if os.path.splitext(c)[1] == '.xml':
            a.append(int(os.path.splitext(c)[0]))
            #print(os.path.splitext(c)[0])
            doc = ET.parse(os.path.join(xmlpath, c))
            root = doc.getroot()
            sub1 = root.find('filename')
            sub1.text = os.path.splitext(c)[0]
            #print(sub1.text)
            #os.path.splitext(k)[0]
            doc.write(os.path.join(xmlpath, c))
            #print(doc)
    print(sorted(a))
def xmlprthc(xmlpath):
    xmllist = os.listdir(xmlpath)
    #imglist = os.listdir(imgpath)
    for k in xmllist:
        if os.path.splitext(k)[1] == '.xml':
            doc = ET.parse(os.path.join(xmlpath, k))
            root = doc.getroot()
            sub2 = root.find('path')
            sub2list = sub2.text.split('/')
            #sub2list[3] = imglist
            #print(sub2list)
            sub2.text = os.path.join(sub2list[0], sub2list[1], sub2list[2], os.path.splitext(k)[0] +'.bmp')
            #print(sub2.text)
            doc.write(os.path.join(xmlpath, k))
def shanchu(xmlpath):
    xmllist = os.listdir(xmlpath)
    for k in xmllist:
        if os.path.splitext(k)[1] != '.xml' or len(os.path.splitext(k)) == 1:
            os.remove(os.path.join(xmlpath, k))

if __name__ == "__main__":
    xmlpath = '/home/nie/downloads/imgxml/xml'  # 存有xml的文件夹路径
    imgpath = '/home/nie/downloads/imgxml/grayimg'
    xmllist = os.listdir(xmlpath)  # 列出文件夹下所有的目录与文件
    imglist = os.listdir(imgpath)
    #gaiming(imglist, xmllist, xmlpath, imgpath)
    changexml(xmlpath)
    #xmlprthc(xmlpath)
    #shanchu(xmlpath)
