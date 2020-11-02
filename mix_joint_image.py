import os,glob
import cv2
import xml.etree.ElementTree as xml
from lxml.etree import Element, SubElement, tostring
from lxml import etree
import numpy as np
import shutil
import random

ok_dir = './endtrain/ok/'   #path of input data
generate_path = './timgs/'
ng_dir = './endtrain/ng/'	

row = 2
col = 2

position_list = None

ng_fraction = 1/4

shape = ( 330, 310 , 3) # unit of joint image
#shape = (400 ,400, 3)
#image_type = '.bmp' 
image_type = '.bmp'

def read_xml(filename ,bias,resize_rate):
    #print("bias:::", bias)
    tree = xml.ElementTree(file=filename)
    root = tree.getroot()
    Anno = root.getchildren()
    box_list = []
    for ano in Anno:
        objs = ano.getchildren()
        box = []
        name = ''
        for obj in objs:
            if(obj.tag == 'name'):
                name = obj.text
                #print(name) 
            bnds = obj.getchildren()
            for bnd in bnds:
                box.append(int(float(bnd.text)))
            #print("box", box)  
        if box :
            box[0] *= resize_rate[0]
            box[0] += bias[0]
            box[1] *= resize_rate[1]
            box[1] += bias[1]
            box[2] *= resize_rate[0]
            box[2] += bias[0]
            box[3] *= resize_rate[1]
            box[3] += bias[1]
            for bbox in box:
                bbox = int(round(bbox))
            box.append(name)
            #print(box)
            box_list.append(box)
    return box_list

def check_shape(a_xml):
    tree = xml.ElementTree(file=a_xml)
    root = tree.getroot()
    width = int(root.findtext('./size/width'))
    height = int(root.findtext('./size/height'))
    return (width <= shape[1] and height <= shape[0])

def check_image(image_name):
    image = cv2.imread(ng_dir + 'image/' + image_name + image_type)
    #print(image.shape)
    return np.all(image != None)
    
def write_xml(xml_name,img_name, width, height, bbox):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'DEye'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = (img_name.split("/")[-1]).split(".")[0]

    node_path = SubElement(node_root, 'path')
    node_path.text = img_name 

    node_source = SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = 'DEye'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(width) 

    node_height = SubElement(node_size, 'height')
    node_height.text = str(height) 

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    node_segmentated = SubElement(node_root, 'segmented')
    node_segmentated.text = '0'

    for i in range(len(bbox)):
        bbox_iter = bbox[i]
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = bbox_iter[4]
        node_name = SubElement(node_object, 'pose')
        node_name.text = 'Unspecified'
        node_name = SubElement(node_object, 'truncated')
        node_name.text = '0'
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
 

        xmin = bbox_iter[0]
        ymin = bbox_iter[1]
        xmax = bbox_iter[2]
        ymax = bbox_iter[3]
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(xmin)
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(ymin) 
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(xmax) 
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(ymax)  

    with open(xml_name, 'wb') as f:
        f.write(etree.tostring(node_root))
    
def joint(a_list,image_path,xml_path,position):      
    #print(i)
    first_image_name = (os.path.split(a_list[0])[-1])[:-4]
    if not(position != None and position >= 0 and position <= row*col):
        position = random.randint(0,row*col-1)
    a_list[0] , a_list[position] = a_list[position] , a_list[0]
    #print('position:{}'.format(position))
    #print(position)
    mat = np.array(a_list).reshape(row,col)
    #print("mat is:", mat)
    joint_image = np.zeros((shape[0]*row, shape[1]*col, shape[2]), dtype = np.uint8)
    #joint_image[:,:,:] = 255
    box_list = []
    for i in range(row):
        for j in range(col):
            ori_image = cv2.imread(mat[i][j])
            #image = np.zeros(shape,dtype = np.uint8)
            image = cv2.resize(ori_image,(shape[1], shape[0]))
            #cv2.imshow('test',image)
            #cv2.waitKey(0)
            h_rate = float(shape[0])/ori_image.shape[0]
            w_rate = float(shape[1])/ori_image.shape[1]
            #print("img shape",image.shape)
            bias = (i*shape[0] , j*shape[1])
            #print("bias", bias)
            image_shape =(min(shape[0] , image.shape[0]) , min(shape[1] , image.shape[1]))
            #print(image_shape)
            joint_image[bias[0] : bias[0] + image_shape[0] , bias[1] : bias[1] + image_shape[1]] = image[0 : image_shape[0] , 0 : image_shape[1]]
            #cv2.imshow('joint_image',joint_image)
            #cv2.waitKey(0)
            #print("shape", joint_image.shape)
            #print("joint_image", len(joint_image))
            path ,image_name = os.path.split(mat[i][j])
            image_name = image_name[:-4]
            #print('path:',path)
            #print('image_path:',image_path)
            if((path + '/') == image_path):
                a_box_list = read_xml(xml_path + image_name + '.xml' , (bias[1] , bias[0]),(w_rate,h_rate))
                #print("box_list", a_box_list)
                box_list.extend(a_box_list)
    #print(joint_image.shape)
    
    #new_image_name = generate_path + 'image/'  + first_image_name + '-{}'.format(position) + image_type
    new_image_name = generate_path + 'image/'  + first_image_name + image_type
    #new_xml_name = generate_path + 'xml/'  + first_image_name + '-{}'.format(position) + '.xml'
    new_xml_name = generate_path + 'xml/'  + first_image_name + '.xml'
    cv2.imwrite(new_image_name , joint_image)
    write_xml(new_xml_name , new_image_name , joint_image.shape[1] , joint_image.shape[0] , box_list)
    #print(new_image_name)
    #cv2.imshow('joint_image', joint_image)
    #cv2.waitKey()
                    
def main():
    xml_path = ng_dir + 'xml/'
    image_path = ng_dir +'image/'
    xml_list = glob.glob(xml_path +'*.xml')
    print('len(xml_list):',len(xml_list))
    ok_image_path = ok_dir
    ok_image_list = glob.glob(ok_image_path + '*' + image_type)
    print('len(ok_list):',len(ok_image_list))
    
    if os.path.exists(generate_path):
        shutil.rmtree(generate_path)
    os.makedirs(generate_path + 'image')
    os.makedirs(generate_path + 'xml')
    
    name_list = []   #joint image name list
    name_llist = []   # joint image name list of list
    joint_count = row * col   #size of name_list
    ng_count = int(joint_count*ng_fraction)
    ok_count = joint_count - ng_count
    print('ok_count:', ok_count)
    print('ng_count:', ng_count)
    
    for a_xml in xml_list:
        #if(check_shape(a_xml)):
        if True:
            image_name = (os.path.split(a_xml)[-1])[:-4]
            #print(image_name)
            if(check_image(image_name)):
                name_list.append(ng_dir + 'image/' + image_name + image_type)
            #print(name_list)
            else:
                print('error image:',image_name)
            if(len(name_list) == ng_count):
                ok_name_list = random.sample(ok_image_list, ok_count)
                name_list.extend(ok_name_list)
                #random.shuffle(name_list)
                name_llist.append(name_list)
                #print(name_list)
                name_list = []
        else:
            print('shape error:',a_xml)
    print(len(name_llist))
    for a_list in name_llist:
        if isinstance(position_list,list):
            for position in position_list:
                copy_list = a_list.copy()
                joint(copy_list,image_path,xml_path,position)
        else:
            joint(a_list,image_path,xml_path,None)

if __name__ == '__main__':
    main()        
