import os
import shutil
from PIL import Image
from PIL import ImageFile


def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    f_list = os.listdir(path)
    # print f_list
    print(len(f_list))
    # if not os.path.dirname(txtpath):
    #     os.makedirs(os.path.dirname(txtpath))
    a = []
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.bmp':
            #print(os.path.splitext(i)[0])
            a.append(i)
            img = Image.open(os.path.join(path, i))
            ImageFile.LOAD_TRUNCATED_IMAGES = True

            #print(path+"/"+i)
            #os.remove(path+"/"+i)
    print(len(a))
if __name__ == '__main__':
    srcpath = '/home/nie/downloads/imgxml'
    getFileName(srcpath)