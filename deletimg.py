import os
from PIL import Image

def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    imgpath = os.path.join(path, 'train2017')
    #xmlpath = os.path.join(path, 'xml')
    imglist = os.listdir(imgpath)
    #xmllist = os.listdir(xmlpath)
    for i in imglist:
        if os.path.splitext(i)[1] == '.jpg':
            try:
                img = Image.open(os.path.join(imgpath, i))
                #print(os.path.join(xmlpath, os.path.splitext(i)[0] + ".xml"))
            except:
                print(os.path.join(imgpath, i))
                os.remove(os.path.join(imgpath, i))
                #print(os.path.join(imgpath, i))
                #os.remove(os.path.join(xmlpath, os.path.splitext(i)[0]+".xml"))
                #print(os.path.join(xmlpath, os.path.splitext(i)[0]+".xml"))

if __name__ == '__main__':
    path = '/home/nie/nmh/datasets/coco'
    getFileName(path)