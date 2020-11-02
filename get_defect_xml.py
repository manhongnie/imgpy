import os,glob
import shutil
import xml.etree.ElementTree as xml

defect_name = ['lw','yw']
root_dir = './zhaochi_0913/train/xml/'

def have_defect(a_xml , defect):
    tree = xml.ElementTree(file = a_xml)
    root = tree.getroot()
    for node in root.findall('./object/name'):
        if(node.text in defect):
            return True
    return False

def get_needed_xml(xml_path):
    xml_list = glob.glob(xml_path + '*.xml')
    print('all xml count:',len(xml_list))
    gen_path = root_dir + defect_name[0] + '/'
    if os.path.exists(gen_path):
        shutil.rmtree(gen_path)
    os.makedirs(gen_path)
    count = 0
    for a_xml in xml_list:
        if have_defect(a_xml , defect_name):
            xml_name = os.path.split(a_xml)[-1]
            shutil.copyfile(a_xml , gen_path + xml_name)
            count += 1
    print('have defect xml count:',count)

def main():
    xml_path = root_dir
    print('xml path',xml_path)
    get_needed_xml(xml_path)

if __name__ == '__main__':
    main()
