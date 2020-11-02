import glob,os,shutil
import cv2
import copy,sys
import numpy as np
import os.path as osp
import xml.etree.ElementTree as xml
from terminaltables import AsciiTable

test_data_path = './zhaochi_0913/train/'
test_results_path = './zhaochi_0913/result/xml/'
output_result_images_path = './zhaochi_0913/result/output/'
image_type = '.bmp'
#defect_labels = ['lw', 'ys', 'zw', 'ps', 'hs', 'yw']
#defect_labels = ['defect', 'qita', 'big' ]
#defect_labels = ['yj','yw','dj', 'sjljx', 'dyj']
#defect_labels = ['ps_lw', 'hs_ys', 'zw', 'yw']
defect_labels = ['qj','jl','qp','lj','mb','yw','lh','lg']
mode = 0 #  1:accurate statistics; other value:rough statistics.
confidence_threshold_range = [0.3, 0.35]
filter_iou_threshold = 0.5
min_scale = (6,6)
show_mode = 0 # 1:full screen;other value:normal window

if osp.exists(output_result_images_path):
    shutil.rmtree(output_result_images_path)
os.makedirs(output_result_images_path)
orign = sys.stdout
sys.stdout = open(osp.join(output_result_images_path, 'log.txt'), mode = 'w',encoding='utf-8')

def get_bounding_box(xml_path, _defect_labels, is_result=False):
    results_dict = {}
    for label in _defect_labels:
        results_dict[label] = []
    tree = xml.ElementTree(file = xml_path)
    root = tree.getroot()
    Anno = root.getchildren()
    min_area = min_scale[0]*min_scale[1]
    for ano in Anno:
        objs = ano.getchildren()
        bbox = []
        name = ''
        confidence = None
        if is_result:
            confidence = 1.0
        for obj in objs:
            if obj.tag == 'confidence':
                confidence = float(obj.text)
            if obj.tag == 'name':
                name = obj.text
            #if name == 'hs':   #0421!!!!!!!!!!!!!!
                #name = 'lw'
            if name in _defect_labels:
                bnds = obj.getchildren()
                for bnd in bnds:
                    bbox.append(int(float(bnd.text)))
        if bbox and ((bbox[2]-bbox[0])*(bbox[3]-bbox[1])) > min_area:
            #print(((bbox[2]-bbox[0])*(bbox[3]-bbox[1])))
            if is_result:
                bbox.append(round(confidence,3))
            results_dict[name].append(bbox)
    return results_dict

def box_area(boxes):
    return (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])

def box_iou(boxes1, boxes2):
    area1 = box_area(boxes1)
    area2 = box_area(boxes2)

    lt = np.maximum(boxes1[:, None, :2], boxes2[:, :2])
    rb = np.minimum(boxes1[:, None, 2:4], boxes2[:, 2:4])

    wh = np.clip((rb - lt), 0, None)
    inter = wh[:, :, 0] * wh[:, :, 1]

    iou = inter / (area1[:, None] + area2 -inter)
    return iou

def filter_bbox_pairs_over_iou_threshold(filename,
                                        test_data_bboxes,
                                        test_results_bboxes,
                                        true_positive,
                                        false_positive,
                                        false_negitive,
                                        _filter_iou_threshold,
                                        _defect_labels):
    need_confirm_mark_bboxes = {}
    need_confirm_results_bboxes = {}
    need_confirm = False
    true_positive[filename] = {}
    false_positive[filename] = {}
    false_negitive[filename] = {}
    for label in _defect_labels:
        len1 = len(test_data_bboxes[label])
        len2 = len(test_results_bboxes[label])
        if(len1 == 0 and len2 !=0):
            false_positive[filename][label] =  {'bbox':[], 'count':0}
            false_positive[filename][label]['bbox'] = copy.deepcopy(test_results_bboxes[label])
            false_positive[filename][label]['count'] = len(test_results_bboxes[label])
        elif(len1 !=0 and len2 ==0):
            false_negitive[filename][label] = {'bbox':[], 'count':0}
            false_negitive[filename][label]['bbox'] = [
                copy.deepcopy(bbox)
                for bbox in test_data_bboxes[label]
            ]
            for bbox in false_negitive[filename][label]['bbox']:
                bbox.append(0.0)
            false_negitive[filename][label]['count'] = len(test_data_bboxes[label])
        elif(len1 != 0 and len2 !=0):
            boxes1 = np.array(test_data_bboxes[label])
            boxes2 = np.array(test_results_bboxes[label])
            ious = box_iou(boxes1, boxes2)
            flags = np.where(ious > 0.3, np.ones_like(ious), np.zeros_like(ious))
            fn_idx = ((np.sum(flags, axis=1) == 0).nonzero())[0].flatten()
            fp_idx = ((np.sum(flags, axis=0) == 0).nonzero())[0].flatten()
            if((len(fn_idx) + len(fp_idx)) > 0):
                need_confirm = True
                if len(fn_idx) > 0:
                    need_confirm_mark_bboxes[label] = copy.deepcopy(boxes1[fn_idx].tolist())
                if len(fp_idx) > 0:
                    need_confirm_results_bboxes[label] = copy.deepcopy(boxes2[fp_idx].tolist())
            tp_idx = ((np.sum(flags, axis=1) > 0).nonzero())[0].flatten()
            result_bboxes_wrt_tp = [copy.deepcopy(boxes2[np.argwhere(flags[idx] > 0)].tolist()) for idx in tp_idx]
            if len(tp_idx) > 0:
                true_positive[filename][label] = []
                for i in range(len(tp_idx)):
                    true_positive[filename][label].append((copy.deepcopy(boxes1[tp_idx[i]].tolist()),
                                                           result_bboxes_wrt_tp[i][0]))
    return need_confirm_mark_bboxes,need_confirm_results_bboxes,need_confirm

def draw_bounding_box(image, label, all_boxes1, all_boxes2, boxes1, boxes2):
    h,w,c = image.shape
    dtype = image.dtype
    result_image = np.zeros((h, w*2+40, 3), dtype = dtype)
    result_image[:,:,:] = 255
    left_image = image
    right_image = image.copy()
    font = cv2.FONT_HERSHEY_COMPLEX
    for box in all_boxes1:
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        cv2.rectangle(left_image,(x_min,y_min),(x_max,y_max),(200,0,0),1)
        cv2.putText(left_image, '{}'.format(label), (x_min, y_min-5),font, 0.4, (0, 0, 100), 1)
    for box in boxes1:
        x_min = int(box[0])
        y_min = int(box[1])
        x_max = int(box[2])
        y_max = int(box[3])
        cv2.rectangle(left_image,(x_min,y_min),(x_max,y_max),(0,0,200),1)
        cv2.putText(left_image, '{}'.format(label), (x_min, y_min-5),font, 0.4, (0, 0, 100), 1)
    result_image[:,0:w] = left_image
    for box in all_boxes2:
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        cv2.rectangle(right_image,(x_min,y_min),(x_max,y_max),(200,0,0),1)
        if isinstance(box[4],float):
            confidence = round(box[4]*100, 2)
            cv2.putText(right_image, '{}:{}%'.format(label,str(confidence)), (x_min, y_min-5),font, 0.4, (47, 47, 100), 1)
    for box in boxes2:
        x_min = int(box[0])
        y_min = int(box[1])
        x_max = int(box[2])
        y_max = int(box[3])
        cv2.rectangle(right_image,(x_min,y_min),(x_max,y_max),(0,0,200),1)
        if isinstance(box[4],float):
            confidence = round(box[4]*100, 2)
            cv2.putText(right_image, '{}:{}%'.format(label,str(confidence)), (x_min, y_min-5),font, 0.4, (47, 47, 100), 1)
    result_image[:,(w+40):w*2+40] = right_image
    return result_image

def only_draw_bounding_box(image, label, all_boxes1, all_boxes2, boxes1, boxes2, text_bias = 0):
    h,w,c = image.shape
    dtype = image.dtype
    small_image_w = int((w - 40)/2)
    left_x_min = 0
    left_x_max = small_image_w
    right_x_min = small_image_w + 40
    right_x_max = right_x_min + small_image_w
    left_image = image[:,left_x_min:left_x_max]
    right_image = image[:,right_x_min:right_x_max]
    font = cv2.FONT_HERSHEY_COMPLEX
    for box in all_boxes1:
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        cv2.rectangle(left_image,(x_min,y_min),(x_max,y_max),(200,0,0),1)
        cv2.putText(left_image, '{}'.format(label), (x_min, y_min-5),font, 0.4, (47, 47, 100), 1)
    for box in boxes1:
        x_min = int(box[0])
        y_min = int(box[1])
        x_max = int(box[2])
        y_max = int(box[3])
        cv2.rectangle(left_image,(x_min,y_min),(x_max,y_max),(0,0,200),1)
        cv2.putText(left_image, '{}'.format(label), (x_min, y_min-5),font, 0.4, (47, 47, 100), 1)
    for box in all_boxes2:
        x_min = box[0]
        y_min = box[1]
        x_max = box[2]
        y_max = box[3]
        cv2.rectangle(right_image,(x_min,y_min),(x_max,y_max),(200,0,0),1)
        if isinstance(box[4],float):
            confidence = round(box[4]*100, 2)
            cv2.putText(right_image, '{}:{}%'.format(label,str(confidence)), (x_min, y_min-5-text_bias),font, 0.4, (47, 47, 100), 1)
    for box in boxes2:
        x_min = int(box[0])
        y_min = int(box[1])
        x_max = int(box[2])
        y_max = int(box[3])
        cv2.rectangle(right_image,(x_min,y_min),(x_max,y_max),(0,0,200),1)
        if isinstance(box[4],float):
            confidence = round(box[4]*100, 2)
            cv2.putText(right_image, '{}:{}%'.format(label,str(confidence)), (x_max, y_max+5),font, 0.4, (47, 47, 100), 1)
    return image

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    image = param[0]
    mark_bboxes = param[1][0]
    results_bboxes = param[1][1]
    false_positive = param[2][0]
    false_negitive = param[2][1]
    filename = param[2][2]
    label = param[2][3]
    window_name = param[2][4]
    cv2.imshow(window_name, image)
    #print("%d,%d" % (x, y))
    if event == cv2.EVENT_LBUTTONDOWN:
        #print("%d,%d" % (x, y))
        if (x<image.shape[1]/2):
            for box in mark_bboxes:
                if box[0]<=x and box[2]>=x and box[1]<=y and box[3]>=y:
                    if filename not in false_negitive:
                         false_negitive[filename] = {}
                    if label not in false_negitive[filename]:
                         false_negitive[filename][label] = {'bbox':[], 'count':0}
                    bbox = copy.deepcopy(box)
                    bbox.append(0.0)
                    false_negitive[filename][label]['bbox'].append(bbox)
                    false_negitive[filename][label]['count'] += 1
                    cv2.rectangle(image, (box[0],box[1]), (box[2],box[3]), (0,255,0), 1, 4)
                    break
        else:
            for box in results_bboxes:
                box[0] = int(box[0])
                box[1] = int(box[1])
                box[2] = int(box[2])
                box[3] = int(box[3])
                x1 = int(x - 40 -(image.shape[1]-40)/2)
                if box[0]<=x1 and box[2]>=x1 and box[1]<=y and box[3] >=y:
                    if filename not in false_positive:
                         false_positive[filename] = {}
                    if label not in false_positive[filename]:
                         false_positive[filename][label] = {'bbox':[], 'count':0}
                    false_positive[filename][label]['bbox'].append(copy.deepcopy(box))
                    false_positive[filename][label]['count'] += 1
                    cv2.rectangle(image, ((box[0]+40+int((image.shape[1]-40)/2)),box[1]),
                                  ((box[2]+40+int((image.shape[1]-40)/2)),box[3]), (0,255,0), 1, 4)
                    break
        #cv2.imshow("confirm_image", image)

def confirm_bounding_box(test_data_bboxes_of_images,
                         test_results_bboxes_of_images,
                         need_confirm_filename_set,
                         need_confirm_mark_bboxes_of_images,
                         need_confirm_results_bboxes_of_images,
                         label, false_positive,
                         false_negitive, ignore_items, _show_mode):
    test_data_image_path = osp.join(test_data_path,'image/')
    for filename in need_confirm_filename_set:
        flag1 = False
        flag2 = False
        if label in need_confirm_mark_bboxes_of_images[filename]:
            flag1 = True
        else:
            need_confirm_mark_bboxes_of_images[filename][label] = []
        if label in need_confirm_results_bboxes_of_images[filename]:
            flag2 = True
        else:
            need_confirm_results_bboxes_of_images[filename][label] = []
        if not(flag1 or flag2):
            continue
        image_path = osp.join(test_data_image_path, filename) + image_type
        image = cv2.imread(image_path)
        confirm_image = draw_bounding_box(image,
                                          label,
                                          test_data_bboxes_of_images[filename][label],
                                          test_results_bboxes_of_images[filename][label],
                                          need_confirm_mark_bboxes_of_images[filename][label],
                                          need_confirm_results_bboxes_of_images[filename][label])
        window_name = "confirm_image"
        cv2.namedWindow(window_name,0)
        if show_mode == 1:
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            #cv2.resizeWindow(window_name, 2500, 1150)
            cv2.moveWindow(window_name,50,0)
        #w, h = confirm_image.shape[1], confirm_image.shape[0]
        #resize_image = cv2.resize(confirm_image,(int(w*resize_ratio),int(h*resize_ratio)))
        param1 = [need_confirm_mark_bboxes_of_images[filename][label] ,
                 need_confirm_results_bboxes_of_images[filename][label]]
        param2 = [false_positive, false_negitive, filename, label, window_name]
        cv2.setMouseCallback(window_name, on_EVENT_LBUTTONDOWN,
                             [confirm_image,
                              param1,
                              param2])
        #cv2.imshow("confirm_image", confirm_image)
        cv2.waitKey()
        cv2.destroyAllWindows()


def classify_bounding_box(test_data_bboxes_of_images,
                          test_results_bboxes_of_images,
                          test_data_filename_set,
                          test_results_filename_set,
                          _defect_labels,
                          _filter_iou_threshold,
                          false_positive,
                          true_positive,
                          false_negitive,
                          _mode,
                          _show_mode):
    true_negitive = {}        # nothing
    ignore_items = {}         # nothing
    undetected_filename_set = test_data_filename_set - test_results_filename_set
    for filename in undetected_filename_set:
        false_negitive[filename] = {}
        for label in _defect_labels:
            false_negitive[filename][label] = {'bbox':[], 'count':0}
            false_negitive[filename][label]['bbox'] = [
                (copy.deepcopy(bbox))
                for bbox in test_data_bboxes_of_images[filename][label]
            ]
            for bbox in false_negitive[filename][label]['bbox']:
                bbox.append(0.0)
            false_negitive[filename][label]['count'] = len(test_data_bboxes_of_images[filename][label])
    need_confirm_mark_bboxes_of_images = {}
    need_confirm_results_bboxes_of_images = {}
    need_confirm_filename_set = set()
    for filename in test_results_filename_set:
        return1, return2, return3 = filter_bbox_pairs_over_iou_threshold(
                                    filename,
                                    test_data_bboxes_of_images[filename],
                                    test_results_bboxes_of_images[filename],
                                    true_positive, false_positive, false_negitive,
                                    _filter_iou_threshold, _defect_labels)
        if return3:
            need_confirm_filename_set.add(filename)
            need_confirm_mark_bboxes_of_images[filename] = return1
            need_confirm_results_bboxes_of_images[filename] = return2
    if _mode == 1:
        for label in _defect_labels:
            confirm_bounding_box(test_data_bboxes_of_images,
                                 test_results_bboxes_of_images,
                                 need_confirm_filename_set,
                                 need_confirm_mark_bboxes_of_images,
                                 need_confirm_results_bboxes_of_images,
                                 label, false_positive,
                                 false_negitive, ignore_items, _show_mode)
    else:
        print('rough statistics.')
    return false_positive, true_positive, false_negitive

def get_dict_elem(data_dict, param1, param2):
    if param1 in data_dict:
        if param2 in data_dict[param1]:
            return data_dict[param1][param2]
    return None

def generate_result_images_file(test_data_filename_set,
                                test_data_image_path,
                                test_data_bboxes_of_images,
                                test_results_bboxes_of_images,
                                output_result_images_path,
                                _defect_labels, _image_type,
                                false_positive, false_negitive):
    false_positive_path = osp.join(output_result_images_path,'false_positive')
    false_negitive_path = osp.join(output_result_images_path,'false_negitive')
    text_bais = 5
    for label in _defect_labels:
        _false_positive_path = osp.join(false_positive_path,label)
        _false_negitive_path = osp.join(false_negitive_path,label)
        os.makedirs(_false_positive_path)
        os.makedirs(_false_negitive_path)
        for filename in test_data_filename_set:
            ori_image_path = osp.join(test_data_image_path, filename) + _image_type
            result_image = None
            if filename in false_positive:
                if label in false_positive[filename]:
                    if false_positive[filename][label]['count'] > 0:
                        image = cv2.imread(ori_image_path)
                        result_image = draw_bounding_box(image,label,
                                       test_data_bboxes_of_images[filename][label],
                                       test_results_bboxes_of_images[filename][label],
                                       [], [])
                        count = 0
                        for _label in _defect_labels:
                            if not(_label == label):
                                count += 1
                                bboxes1 = get_dict_elem(test_data_bboxes_of_images,filename,_label)
                                bboxes1 = [] if bboxes1 is None else bboxes1
                                bboxes2 = get_dict_elem(test_results_bboxes_of_images,filename,_label)
                                bboxes2 = [] if bboxes2 is None else bboxes2
                                result_image = only_draw_bounding_box(result_image,_label,
                                               bboxes1,
                                               bboxes2,
                                               [], [], text_bais*count)
                        result_image = only_draw_bounding_box(result_image,label,
                                       [], [], [], false_positive[filename][label]['bbox'])
                        result_image_output_path = osp.join(_false_positive_path,
                                                   filename) + _image_type
                        cv2.imwrite(result_image_output_path, result_image)
            if filename in false_negitive:
                if label in false_negitive[filename]:
                    if false_negitive[filename][label]['count'] > 0:
                        image = cv2.imread(ori_image_path)
                        if filename in test_results_bboxes_of_images:
                            if label in test_results_bboxes_of_images[filename]:
                                result_image = draw_bounding_box(image,label,
                                       test_data_bboxes_of_images[filename][label],
                                       test_results_bboxes_of_images[filename][label],
                                       [],[])
                                count = 0
                                for _label in _defect_labels:
                                    if not(_label == label):
                                        count += 1
                                        bboxes1 = get_dict_elem(test_data_bboxes_of_images,filename,_label)
                                        bboxes1 = [] if bboxes1 is None else bboxes1
                                        bboxes2 = get_dict_elem(test_results_bboxes_of_images,filename,_label)
                                        bboxes2 = [] if bboxes2 is None else bboxes2
                                        result_image = only_draw_bounding_box(result_image,_label,
                                                       bboxes1,
                                                       bboxes2,
                                                       [], [], text_bais*count) 
                                result_image = only_draw_bounding_box(result_image,label,
                                       [], [],
                                       false_negitive[filename][label]['bbox'],[])
                        if result_image is None:
                            result_image = draw_bounding_box(image,label,
                                       test_data_bboxes_of_images[filename][label],
                                       [], [],[])
                            count = 0
                            for _label in _defect_labels:
                                if not(_label == label):
                                    count += 1
                                    bboxes1 = get_dict_elem(test_data_bboxes_of_images,filename,_label)
                                    bboxes1 = [] if bboxes1 is None else bboxes1
                                    bboxes2 = get_dict_elem(test_results_bboxes_of_images,filename,_label)
                                    bboxes2 = [] if bboxes2 is None else bboxes2
                                    result_image = only_draw_bounding_box(result_image,_label,
                                                   bboxes1,
                                                   bboxes2,
                                                   [], [], text_bais*count)                                        
                            result_image = only_draw_bounding_box(result_image,label,
                                       test_data_bboxes_of_images[filename][label],
                                       [],
                                       false_negitive[filename][label]['bbox'],[])               
                        result_image_output_path = osp.join(_false_negitive_path,
                                                   filename) + _image_type
                        cv2.imwrite(result_image_output_path, result_image)

def analyze_fp_fn(test_data_filename_set, _defect_labels, false_positive, false_negitive):
    statistical_info = {}
    fp_bbox_amount = {}
    fn_bbox_amount = {}
    fp_image_amount = {}
    fn_image_amount = {}
    for label in _defect_labels:
        fp_bbox_amount[label] = 0
        fn_bbox_amount[label] = 0
        fp_image_amount[label] = 0
        fn_image_amount[label] = 0
        for filename in test_data_filename_set:
            if filename in false_positive:
                if label in false_positive[filename]:
                    fp_bbox_amount[label] += false_positive[filename][label]['count']
                    if false_positive[filename][label]['count'] > 0:
                        fp_image_amount[label] += 1
            if filename in false_negitive:
                if label in false_negitive[filename]:
                    fn_bbox_amount[label] += false_negitive[filename][label]['count']
                    if false_negitive[filename][label]['count'] > 0:
                        fn_image_amount[label] += 1
    statistical_info['fp_bbox_amount'] = fp_bbox_amount
    statistical_info['fn_bbox_amount'] = fn_bbox_amount
    statistical_info['fp_image_amount'] = fp_image_amount
    statistical_info['fn_image_amount'] = fn_image_amount
    return statistical_info

def print_map_summary(statistical_info, key1, key2, labels):
    header = ['label class', 'number of bounding boxes', 'number of images']
    table_data = [header]
    for label in labels:
        row_data = [
            label,
            statistical_info[key1][label],
            statistical_info[key2][label]
        ]
        table_data.append(row_data)
    table = AsciiTable(table_data)
    # table.inner_footing_row_border = True
    print(table.table)

def analyze_fp_fn_by_confidence_threshold(false_positive,
                                          true_positive,
                                          false_negitive,
                                          confidence_threshold_range,
                                          test_data_filename_set,
                                          _defect_labels):
    statistical_info = {}
    fp = copy.deepcopy(false_positive)
    tp = copy.deepcopy(true_positive)
    fn = copy.deepcopy(false_negitive) # nothing
    fore_key = None
    later_key = None
    for confidence_threshold in confidence_threshold_range:
        later_key = str(confidence_threshold)
        statistical_info[later_key] = {}
        fp_bbox_difference = {}
        fn_bbox_difference = {}
        fp_image_difference = {}
        fn_image_difference = {}
        for label in _defect_labels:
            if fore_key is None:
                fp_bbox_difference[label] = 0
                fn_bbox_difference[label] = 0
                fp_image_difference[label] = 0
                fn_image_difference[label] = 0
            else:
                fore = statistical_info[fore_key]
                fp_bbox_difference[label] = fore['fp_bbox_difference'][label]
                fn_bbox_difference[label] = fore['fn_bbox_difference'][label]
                fp_image_difference[label] = fore['fp_image_difference'][label]
                fn_image_difference[label] = fore['fn_image_difference'][label]
            for filename in test_data_filename_set:
                if filename in fp:
                    if label in fp[filename]:
                        if fp[filename][label]['count'] > 0:
                            for bbox in fp[filename][label]['bbox']:
                                if bbox[4] < confidence_threshold:
                                    fp[filename][label]['bbox'].remove(bbox)
                                    fp[filename][label]['count'] -= 1
                                    fp_bbox_difference[label] -= 1
                            if fp[filename][label]['count'] == 0:
                                fp[filename].pop(label)
                                fp_image_difference[label] -= 1
                if filename in tp:
                    if label in tp[filename]:
                     if len(tp[filename][label]) > 0:
                         for pairs in tp[filename][label]:
                             for bbox in pairs[1]:
                                 if bbox[4] < confidence_threshold:
                                     pairs[1].remove(bbox)
                             if len(pairs[1]) == 0:
                                 tp[filename][label].remove(pairs)
                                 fn_bbox_difference[label] += 1
                                 if filename not in fn:
                                     fn[filename] = {}
                                 if label not in fn[filename]:
                                     fn[filename][label] = {'bbox':[], 'count':0}
                                 pairs[0].append(0.0)     
                                 fn[filename][label]['bbox'].append(pairs[0])
                                 fn[filename][label]['count'] += 1
                         if len(tp[filename][label]) == 0:
                             tp[filename].pop(label)
                             fn_image_difference[label] += 1         
        statistical_info[later_key]['fp_bbox_difference'] = fp_bbox_difference
        statistical_info[later_key]['fn_bbox_difference'] = fn_bbox_difference
        statistical_info[later_key]['fp_image_difference'] = fp_image_difference
        statistical_info[later_key]['fn_image_difference'] = fn_image_difference
        fore_key = later_key
    return statistical_info

def print_map_summary_for_confidence_threshold(statistical_difference_info,
                                               labels):
    header = [
        'label class', 'fp_bbox_difference', 'fn_bbox_difference', 
        'fp_image_difference', 'fn_image_difference'
    ]
    key1 = 'fp_bbox_difference'
    key2 = 'fn_bbox_difference'
    key3 = 'fp_image_difference'
    key4 = 'fn_image_difference'
    table_data = [header]
    for label in labels:
        row_data = [
            label,
            statistical_difference_info[key1][label],
            statistical_difference_info[key2][label],
            statistical_difference_info[key3][label],
            statistical_difference_info[key4][label]
        ]
        table_data.append(row_data)
    table = AsciiTable(table_data)
    # table.inner_footing_row_border = True
    print(table.table)

def main():
    test_data_xml_path = osp.join(test_data_path,'xml/')
    test_data_image_path = osp.join(test_data_path,'image/')
    test_results_xml_path = test_results_path
    test_data_xml_path_list = glob.glob(osp.join(test_data_xml_path,'*.xml'))
    test_data_filename_set = set([(osp.split(xml_path)[-1]).strip()[:-4]
                                for xml_path in test_data_xml_path_list])
    test_results_xml_path_list = glob.glob(osp.join(test_results_xml_path,'*.xml'))
    test_results_filename_set = set([(osp.split(xml_path)[-1]).strip()[:-4]
                                for xml_path in test_results_xml_path_list])
    test_data_bboxes_of_images = {}
    test_results_bboxes_of_images = {}
    for xml_path in test_data_xml_path_list:
        filename = (osp.split(xml_path)[-1]).strip()[:-4]
        test_data_bboxes_of_images[filename] = get_bounding_box(xml_path,defect_labels)
    for xml_path in test_results_xml_path_list:
        filename = (osp.split(xml_path)[-1]).strip()[:-4]
        test_results_bboxes_of_images[filename] = get_bounding_box(xml_path,defect_labels,True)
    #print(test_data_bboxes_of_images)
    false_positive = {}
    true_positive = {}
    false_negitive = {}
    classify_bounding_box(test_data_bboxes_of_images,
                          test_results_bboxes_of_images,
                          test_data_filename_set,
                          test_results_filename_set,
                          defect_labels,
                          filter_iou_threshold,
                          false_positive,
                          true_positive,
                          false_negitive,
                          mode,
                          show_mode)
    generate_result_images_file(test_data_filename_set,
                                test_data_image_path,
                                test_data_bboxes_of_images,
                                test_results_bboxes_of_images,
                                output_result_images_path,
                                defect_labels, image_type,
                                false_positive, false_negitive)
    statistical_info = analyze_fp_fn(test_data_filename_set, defect_labels,
                                     false_positive, false_negitive)
    print('false positive statistical info:')
    print_map_summary(statistical_info, 'fp_bbox_amount', 'fp_image_amount', defect_labels)
    print('false negitive statistical info:')
    print_map_summary(statistical_info, 'fn_bbox_amount', 'fn_image_amount', defect_labels)
    statistical_difference_info = analyze_fp_fn_by_confidence_threshold(false_positive,
                                                                        true_positive,
                                                                        false_negitive,
                                                                        confidence_threshold_range,
                                                                        test_data_filename_set,
                                                                        defect_labels)
    for confidence_threshold in confidence_threshold_range:
        print('confidence_threshold:{}'.format(confidence_threshold))
        print_map_summary_for_confidence_threshold(
                    statistical_difference_info[str(confidence_threshold)],
                    defect_labels)

if __name__ == '__main__':
    main()
    sys.stdout = orign
    f = open(osp.join(output_result_images_path, 'log.txt'), mode = 'r',encoding='utf-8')
    print(f.read())
    f.close()

