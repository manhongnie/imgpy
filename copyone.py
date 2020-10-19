import os
import shutil

def CreateDir(path):
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        print(path+' 目录创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')


def CopyFile(filepath, newPath):
    # 获取当前路径下的文件名，返回List
    fileNames = os.listdir(filepath)
    for file in fileNames:
        # 将文件命加入到当前文件路径后面
        newDir = filepath + '/' + file
        print(newDir)
        # 如果是文件
        if os.path.isfile(newDir):
            print(newDir)
            newFile = newPath + "/" +file
            print(newFile)
            shutil.copyfile(newDir, newFile)
        #如果不是文件，递归这个文件夹的路径
        #else:
            #CopyFile(newDir, newPath)

if __name__ == "__main__":
    #path = input("输入需要复制文件目录：")
    path = "/media/nie/9E6052E56052C425/jufei3030caisepjie"
    xmlpath = os.path.join(path, "xml")
    imagepath = os.path.join(path, "image")
    # 创建目标文件夹
    mkPath = os.path.join(path, "mix")
    CreateDir(mkPath)
    CopyFile(xmlpath, mkPath)
    CopyFile(imagepath, mkPath)