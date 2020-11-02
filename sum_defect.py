import os
import glob
import random
import pandas as pd
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as xml

defect_count={'qj':0,'jl':0,'qp':0,'lj':0,'mb':0,'yw':0,'lh':0,'lg':0}
valid_xml_count = 0
#统计训练图片的缺陷个数
root_dir = './zhoachi_0913/train/xml/'
#生成路径
#root_dir = './getXML_gen/loujian/xml'
#root_dir = '/home/stin/Desktop/scripts/gen/B'
#root_dir = '/home/stin/test/0906/LED/purple_light/ng/xml'


def count_flag(filename):
    tree = xml.ElementTree(file=filename)
    root = tree.getroot()
    global valid_xml_count
    if(len(root.findall('./object/name')) != 0):
        valid_xml_count += 1
    for node in root.findall('./object/name'):
        if node.text in defect_count.keys():
            for defectName in defect_count.keys():
                if node.text == defectName:
                    defect_count[defectName] += 1

def sum_defect():
    xml_list = glob.glob(root_dir + '/*.xml')
    print('xml count:',len(xml_list)) 
    for filename in xml_list:
        count_flag(filename)
    result_list = []
    for key,value in defect_count.items():
        item = (key,value)
        result_list.append(item)
    column_name = ['defectName','count']   
    result_df = pd.DataFrame(result_list, columns=column_name)
    #result_df.to_csv(result_csv_output,index=None)
    print(result_df)  
    print('valid_xml_count:',valid_xml_count)

def main():
    valid_xml_count = 0
    sum_defect()

if __name__ == '__main__':
    main()

    
