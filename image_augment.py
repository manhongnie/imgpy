import os,glob,shutil
import os.path as osp
import numpy as np
import cv2
          
''' 
image=cv2.imread("./image/2009_0_1584414577.tif")
B,G,R = cv2.split(image)                       

cv2.imshow("RED",R)                            
cv2.imshow("GREEN",G)                         
cv2.imshow("BLUE",B)

gray = R + 0.6*G 
gray = gray.astype(np.uint8)
gray[gray>255] = 255
gray[gray<0] = 0
#gray = cv2.blur(gray,(5,5))
#cv2.imshow("RED",gray)
cv2.imshow('ori image',image) 
cv2.imshow("test",np.hstack((R,G,B,gray)))
zeros = np.zeros(image.shape[:2],dtype="uint8")
#cv2.imshow("BLUE",cv2.merge([B,zeros,zeros]))
#cv2.imshow("GREEN",cv2.merge([zeros,G,zeros]))
#cv2.imshow("RED",cv2.merge([zeros,zeros,R]))
#cv2.imshow('BLUE_ADN_RED',cv2.merge([R,zeros,B]))
#cv2.imshow('BLUE_ADN_RED_',cv2.merge([B,zeros,R]))
cv2.waitKey(0)
'''

input_path = './zhaochi_0913/small_images/ng/image/'
output_path = './zhaochi_0913/gray_ng_4/'
image_type = '.bmp'
rgb_weights = (1,0,0)

def convert_rgb_to_gray(_input_path, _output_path, filename, _image_type, _rgb_weights):
    input_image_path = osp.join(_input_path,filename) + image_type
    image = cv2.imread(input_image_path)
    B, G, R = cv2.split(image)
    gray = _rgb_weights[0]*R + _rgb_weights[1]*G + _rgb_weights[2]*B 
    gray = gray.astype(np.uint8)
    gray[gray>255] = 255
    gray[gray<0] = 0
    output_image_path = osp.join(_output_path,filename) + image_type
    cv2.imwrite(output_image_path,gray)

def main():
    if osp.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    image_list = glob.glob(osp.join(input_path,'*')+image_type)
    for image_path in image_list:
        filename = (osp.split(image_path)[-1])[:-4]
        convert_rgb_to_gray(input_path, output_path, filename, image_type, rgb_weights)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
