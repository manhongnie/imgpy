import os
import xml.etree.ElementTree as ET

def changexml(xmlpath):
    xmllist = os.listdir(xmlpath)
    for c in xmllist:
        if os.path.splitext(c)[1] == '.xml':
            doc = ET.parse(os.path.join(xmlpath, c))
            root = doc.getroot()
            for s in root.findall('size'):
                s.find('depth').text = str(1)
            doc.write(os.path.join(xmlpath, c))

if __name__ == "__main__":
    xmlpath = 'D:/jinkeloc/xml'  # 存有xml的文件夹路径
    changexml(xmlpath)