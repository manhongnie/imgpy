#!/usr/bin/env python

import cv2
import math
import numpy as np
import os
import pdb
import xml.etree.ElementTree as ET
import random
import shutil

imgs_path_ng = './train/ng/image'
#imgs_path_ok = './zhihao_0817/joint-xml/'
xmls_path = './train/ng/xml/'
#img_save_path = './train/image/'
#xml_save_path = './train/xml/'
generate_path = './endtrain'
size = (310, 330)

class ImgAugemention():
    def __init__(self):
        self.angle = 0

    # rotate_img
    def rotate_image(self, src, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        # convet angle into rad
        rangle = np.deg2rad(angle)  # angle in radians
        # calculate new image width and height
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # map
        return cv2.warpAffine(
            src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
            flags=cv2.INTER_LANCZOS4)

    def rotate_xml(self, src, xmin, ymin, xmax, ymax, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        # get width and heigh of changed image
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # rot_mat: the final rot matrix
        # get the four center of edges in the initial martix，and convert the coord
        point1 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymin, 1]))
        point2 = np.dot(rot_mat, np.array([xmax, (ymin+ymax)/2, 1]))
        point3 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymax, 1]))
        point4 = np.dot(rot_mat, np.array([xmin, (ymin+ymax)/2, 1]))
        # concat np.array
        concat = np.vstack((point1, point2, point3, point4))
        # change type
        concat = concat.astype(np.int32)
        print(concat)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        return rx, ry, rw, rh


    def process_img(self, imgs_path, img_save_path, xml_save_path, xmls_path):
        # assign the rot angles
        #angle_list = [0, 90, 180, 270]
        angle_list = [0, 180]
        for img_name in os.listdir(imgs_path):
            #k = random.randint(0,3)
            #angle = angle_list[k]
            for angle in angle_list:
                # split filename and suffix
                n, s = os.path.splitext(img_name)
                # for the sake of use yol model, only process '.jpg'
                if s == ".bmp":
                    img_path = os.path.join(imgs_path, img_name)
                    img = cv2.imread(img_path)
                    if angle == 0 or angle == 180:
                        x_rate = float(size[1]/img.shape[1])
                        y_rate = float(size[0]/img.shape[0])
                    elif angle == 90 or angle == 270:
                        x_rate = float(size[1]/img.shape[0])
                        y_rate = float(size[0]/img.shape[1])
                    #print(img.shape)
                    rotated_img = self.rotate_image(img, angle)
                    # resize
                    rotated_img = cv2.resize(rotated_img,size,interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(img_save_path + n + "_" + str(angle) + "d.bmp", rotated_img)
                    print("log: [%sd] %s is processed." % (angle, img))
                    if(xmls_path != None):
                        xml_url = img_name.split('.')[0] + '.xml'
                        xml_path = os.path.join(xmls_path, xml_url)
                        tree = ET.parse(xml_path)
                        root = tree.getroot()
                        Anno = root.getchildren()
                        for ano in Anno:
                            if ano.tag == 'size':
                                ano[0].text = str(size[1])
                                ano[1].text = str(size[0])
                        for box in root.iter('bndbox'):
                            xmin = float(box.find('xmin').text)
                            ymin = float(box.find('ymin').text)
                            xmax = float(box.find('xmax').text)
                            ymax = float(box.find('ymax').text)
                            x, y, w, h = self.rotate_xml(img, xmin, ymin, xmax, ymax, angle)
                            # change the coord
                            x1 = x * x_rate
                            y1 = y * y_rate
                            x2 = (x+w) * x_rate
                            y2 = (y+h) * y_rate
                            
                            box.find('xmin').text = str(x1)
                            box.find('ymin').text = str(y1)
                            box.find('xmax').text = str(x2)
                            box.find('ymax').text = str(y2)
                            box.set('updated', 'yes')
                            # write into new xml
                        tree.write(xml_save_path + n + "_" + str(angle) + "d.xml")
                print("[%s] %s is processed." % (angle, img_name))


if __name__ == '__main__':
    img_aug = ImgAugemention()
    if os.path.exists(generate_path):         
        shutil.rmtree(generate_path)     
    os.makedirs(generate_path + '/ng/image/')  
    os.makedirs(generate_path + '/ng/xml/')
    #os.makedirs(generate_path + '/ok/image/')
    img_aug.process_img(imgs_path_ng, generate_path + '/ng/image/',generate_path + '/ng/xml/' ,xmls_path)
    #img_aug.process_img(imgs_path_ok, generate_path + '/ok/image/')

