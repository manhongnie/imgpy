import glob,os,sys
import shutil
import os.path as osp
import xml.etree.ElementTree as xml
from terminaltables import AsciiTable

output_result_path = './zhihao_0529/train2/analyze/'
input_data_path = './zhihao_0529/train2/xml/'
#defect_labels =  ['lw','ys','zw', 'ps', 'hs', 'yw']
defect_labels = ['lw','ys','zw', 'ps', 'hs', 'yw', 'dj']
defect_count_range = [0, 1 ,2 ,3]
confidence_interval_range =[(0.0, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6,0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
scale_interval_range_info = (0.0 ,96.0, 5.0)

if osp.exists(output_result_path):
        shutil.rmtree(output_result_path)
os.makedirs(output_result_path)
orign = sys.stdout
sys.stdout = open(osp.join(output_result_path, 'log.txt'), mode = 'w',encoding='utf-8')

def count_defects(a_xml, info_dict, _defect_labels):
    for label in _defect_labels:
        info_dict[label] = 0
    info_dict['count'] = 0
    tree = xml.ElementTree(file=a_xml)
    root = tree.getroot()
    for node in root.findall('./object/name'):
        if node.text in _defect_labels:
            info_dict[node.text] += 1
    for label in _defect_labels:
        info_dict['count'] += info_dict[label] 

def print_map_summary_for_numbers_of_defect(statistical_info, _defect_count_range, labels):
    header = ['defect_count']
    for label in labels:
        header.append(label)
    header.append('image_count')
    table_data = [header]
    for defect_count in _defect_count_range:
        key = str(defect_count)
        row_data = [key]
        for label in labels:
            row_data.append(statistical_info[key][label])
        row_data.append(statistical_info[key]['image_count'])
        table_data.append(row_data)
    row_data = ['other']
    for label in labels:
        row_data.append(statistical_info['other'][label])
    row_data.append(statistical_info['other']['image_count'])
    table_data.append(row_data)    
    table = AsciiTable(table_data)
    # table.inner_footing_row_border = True
    print(table.table)

def analyze_numbers_of_defect_by_image_level(xml_list, _defect_labels, _defect_count_range):
    statistical_info = {}
    analysis_results = {}
    for defect_count in _defect_count_range:
        key = str(defect_count)
        analysis_results[key] = {}
        for label in _defect_labels:
            analysis_results[key][label] = 0
        analysis_results[key]['image_count'] = 0
    analysis_results['other'] = {}
    for label in _defect_labels:
        analysis_results['other'][label] = 0
    analysis_results['other']['image_count'] = 0
    for a_xml in xml_list:
        statistical_info[a_xml] = {}
        count_defects(a_xml, statistical_info[a_xml], _defect_labels)
        defect_count = statistical_info[a_xml]['count']
        if defect_count in _defect_count_range:
            key = str(defect_count)
            analysis_results[key]['image_count'] += 1
            for label in _defect_labels:
                analysis_results[key][label] += statistical_info[a_xml][label]
        else:
            analysis_results['other']['image_count'] += 1
            for label in _defect_labels:
                analysis_results['other'][label] += statistical_info[a_xml][label]
    print_map_summary_for_numbers_of_defect(analysis_results, _defect_count_range, _defect_labels)                  

def search_confidence_intervals(confidence, _confidence_interval_range):
    confidence_intervals = []
    for confidence_interval in _confidence_interval_range:
        lower_bound = min(confidence_interval[0], confidence_interval[1])
        upper_bound = max(confidence_interval[0], confidence_interval[1])
        if confidence >= lower_bound and confidence < upper_bound:
            confidence_intervals.append(confidence_interval)
    return confidence_intervals

def count_defects_by_confidence_interval(a_xml, info_dict, _defect_labels, _confidence_interval_range):
    tree = xml.ElementTree(file=a_xml)
    root = tree.getroot()
    Anno = root.getchildren()
    for ano in Anno:
        objs = ano.getchildren()
        confidence = 0
        confidence_intervals = []
        label = None
        for obj in objs:
            if obj.tag == 'confidence':
                confidence = float(obj.text)
                confidence_intervals = search_confidence_intervals(confidence, _confidence_interval_range)
            if obj.tag == 'name':
                label = obj.text     
        if label in _defect_labels:
            for confidence_interval in confidence_intervals:
                key = str(confidence_interval)
                info_dict[key][label] += 1
                info_dict[key]['count'] += 1

def search_scale_interval(bbox, scale_interval_range):
    box_area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])
    for scale_interval in scale_interval_range:
        lower_bound = scale_interval[0]**2
        upper_bound = scale_interval[1]**2
        if box_area >= lower_bound and box_area < upper_bound:
            return scale_interval
    return None
                    
def count_defects_by_scale_interval(a_xml, info_dict, _defect_labels, scale_interval_range):
    tree = xml.ElementTree(file=a_xml)
    root = tree.getroot()
    Anno = root.getchildren()
    for ano in Anno:
        objs = ano.getchildren()
        label = None
        bbox = None
        scale_interval = None
        for obj in objs:
            if obj.tag == 'name':
                label = obj.text
            if label in _defect_labels:
                bnds = obj.getchildren()
                bbox = []
                for bnd in bnds:
                    bbox.append(int(float(bnd.text)))     
        if bbox:
            scale_interval = search_scale_interval(bbox, scale_interval_range)
            if scale_interval:
                key = str(scale_interval)
            else:
                key = 'qita'
            info_dict[key][label] += 1
            info_dict[key]['count'] += 1        

def print_map_summary_for_confidence_distribution(statistical_info, labels, _confidence_interval_range):
    header = ['confidence interval']
    for label in labels:
        header.append(label)
    header.append('defect count')
    table_data = [header]
    for confidence_interval in _confidence_interval_range:
        key = str(confidence_interval)
        row_data = [key]
        for label in labels:
            row_data.append(statistical_info[key][label])
        row_data.append(statistical_info[key]['count'])
        table_data.append(row_data)
    table = AsciiTable(table_data)
    # table.inner_footing_row_border = True
    print(table.table)  

def analyze_confidence_distribution_by_defect_level(xml_list, _defect_labels, _confidence_interval_range):
    statistical_info = {}
    for confidence_interval in _confidence_interval_range:
        key = str(confidence_interval)
        statistical_info[key] = {}
        for label in _defect_labels:
            statistical_info[key][label] = 0
        statistical_info[key]['count'] = 0
    for a_xml in xml_list:
        count_defects_by_confidence_interval(a_xml, statistical_info, _defect_labels, _confidence_interval_range)
    print_map_summary_for_confidence_distribution(statistical_info, _defect_labels, _confidence_interval_range)

def print_map_summary_for_scale_distribution(statistical_info, labels, scale_interval_range):
    header = ['scale interval']
    for label in labels:
        header.append(label)
    header.append('defect count')
    table_data = [header]
    for scale_interval in scale_interval_range:
        key = str(scale_interval)
        row_data = [key]
        for label in labels:
            row_data.append(statistical_info[key][label])
        row_data.append(statistical_info[key]['count'])
        table_data.append(row_data)
    row_data = ['qita']
    for label in labels:
        row_data.append(statistical_info['qita'][label])
    row_data.append(statistical_info['qita']['count'])
    table_data.append(row_data)    
    table = AsciiTable(table_data)
    # table.inner_footing_row_border = True
    print(table.table)       

def analyze_scale_distribution_by_defect_level(xml_list, _defect_labels, _scale_interval_range_info):
    statistical_info = {}
    min_scale = _scale_interval_range_info[0]
    max_scale = _scale_interval_range_info[1]
    stride = _scale_interval_range_info[2]
    _min = min_scale
    _max = min_scale + stride
    scale_interval_range = []
    while _min < max_scale or _max < max_scale:
        scale_interval = (_min,_max)
        scale_interval_range.append(scale_interval)
        key = str(scale_interval)
        statistical_info[key] = {}
        for label in _defect_labels:
            statistical_info[key][label] = 0
        statistical_info[key]['count'] = 0
        _min += stride
        _max += stride
    statistical_info['qita'] = {}
    for label in _defect_labels:
        statistical_info['qita'][label] = 0
    statistical_info['qita']['count'] = 0
    for a_xml in xml_list:
        count_defects_by_scale_interval(a_xml, statistical_info, _defect_labels, scale_interval_range)
    #print(statistical_info) 
    print_map_summary_for_scale_distribution(statistical_info, _defect_labels, scale_interval_range)   

def main():
    xml_list = glob.glob(input_data_path + '*.xml')
    analyze_numbers_of_defect_by_image_level(xml_list, defect_labels, defect_count_range)
    analyze_confidence_distribution_by_defect_level(xml_list, defect_labels, confidence_interval_range)
    analyze_scale_distribution_by_defect_level(xml_list, defect_labels, scale_interval_range_info)   
    
if __name__ == '__main__':
    main()
    sys.stdout = orign
    f = open(osp.join(output_result_path, 'log.txt'), mode = 'r',encoding='utf-8')
    print(f.read())
    f.close()
