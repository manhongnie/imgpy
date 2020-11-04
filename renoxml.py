import os
import xml.etree.ElementTree as ET

def changexml(xmlpath):
    xmllist = os.listdir(xmlpath)
    for c in xmllist:
        if os.path.splitext(c)[1] == '.xml':
            doc = ET.parse(os.path.join(xmlpath, c))
            root = doc.getroot()
            s = root.findall('object')
            if s:
                print(s)
            else:
                os.remove(os.path.join(xmlpath, c))

if __name__ == "__main__":
    xmlpath = 'D:/jinkeimg/1103/xml'  # 存有xml的文件夹路径
    changexml(xmlpath)