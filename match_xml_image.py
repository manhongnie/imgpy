import os,glob,sys

image_type = '.bmp'
root_dir = '/media/img/ada5301c-c9d3-4dd3-809f-d0c476328d58/JPF/DEye_zhaochi(fj)/images/zhaochi1016/smallPictureB/ng/'

def match_xml_image(xml_path, image_path):
    xml_list = glob.glob(xml_path + '*.xml')
    print(xml_list)
    for a_xml in xml_list:
        filename = (os.path.split(a_xml)[-1]).strip()[:-4]
        image_name = image_path + filename + image_type
        print(image_name)
        if os.path.isfile(image_name):
            continue
        else:
            os.remove(a_xml)
            sys.stdout.write('[INFO] Remove' + a_xml + '\n')
    image_list = glob.glob(image_path + '*' + image_type)
    for a_image in image_list:
        filename = (os.path.split(a_image)[-1]).strip()[:-4]
        xml_name = xml_path +filename + '.xml'
        if os.path.isfile(xml_name):
            continue
        else:
            os.remove(a_image)
            sys.stdout.write('[INFO] Remove' +a_image + '\n')

def main():
    xml_path = root_dir + 'xml/'
    image_path = root_dir + 'image/'
    print('xml_path:' , xml_path)
    match_xml_image(xml_path , image_path)

if __name__ == '__main__':
    main()
