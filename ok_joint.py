import os,glob
import cv2
import numpy as np
import shutil
import random

ok2_dir = './GppTest/ok/'
ok1_dir = './GppTest/Testimg/'
generate_path = './GppTest/timg/'

row = 2
col = 2

shape =( 450 , 440 , 3)# unit of joint image
image_type = '.bmp' 

def check_shape(a_image):
    image = cv2.imread(a_image)
    return (image.shape[1] <= shape[1] and image.shape[0] <= shape[0])

def joint(a_list):
    mat = np.array(a_list).reshape(row,col)
    joint_image = np.zeros((shape[0]*row, shape[1]*col, shape[2]), dtype = np.uint8)
    for i in range(row):
        for j in range(col):
            #print(mat[i][j])
            ori_image = cv2.imread(mat[i][j])
            image = cv2.resize(ori_image,(shape[1], shape[0]))
            bias = (i*shape[0] , j*shape[1])
            joint_image[bias[0] : bias[0] + image.shape[0] , bias[1] : bias[1] + image.shape[1]] = image

    new_image_name = generate_path + (os.path.split(mat[0][0])[-1])[:-4] + image_type
    cv2.imwrite(new_image_name , joint_image)

    

def main():
    ok1_image_list = glob.glob(ok1_dir + '*' + image_type)
    ok2_image_list = glob.glob(ok2_dir + '*' + image_type)
    print('len(ok1_image_list):',len(ok1_image_list))
    print('len(ok2_image_list):',len(ok2_image_list))

    if os.path.exists(generate_path):
        shutil.rmtree(generate_path)
    os.makedirs(generate_path )
    
    name_list = []   #joint image name list
    name_llist = []   # joint image name list of list
    joint_count = row * col   #size of name_list
    
    for a_image in ok1_image_list:
        #if(check_shape(a_image)):
            name_list.append(a_image)
            fill_image = random.sample(ok2_image_list, joint_count-1)
            name_list.extend(fill_image)
            if(len(name_list) == joint_count):
                name_llist.append(name_list)
                name_list = []
    
    for a_list in name_llist:
        joint(a_list)

if __name__ == '__main__':
    main()       
