# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from collections import OrderedDict

xmlLabel_Dir = '/apps/liusj/testLabelImgs/Annotations'
jpegImg_Dir = '/apps/liusj/testLabelImgs/JPEGImages'

if not os.path.exists('labels/'):  #生成的label放在label目录下
    os.makedirs('labels/')
file_name = 'voc2007.trainval'
write_lines = []
out_file = open('labels/%s.txt'%(file_name),'w')
image_index = 0
class_dic = OrderedDict()
for rootDir,dirs,files in os.walk(xmlLabel_Dir):
    for file in files:
        fileName = file.split('.')[0]
        imgName = fileName + '.jpg'
        if not os.path.isfile(os.path.join(jpegImg_Dir, imgName)):
            print 'Error:',imgName
            continue
        write_lines += '# ' + str(image_index) + '\n'
        image_index += 1
        in_file = open("%s/%s"%(rootDir,file))
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        write_lines += imgName + '\n'
        num_obj = 0
        write_box = ''
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            #if cls not in classes or int(difficult)==1:
            #    continue
            if cls in class_dic.keys():
                cls_id = class_dic[cls][0]
                class_dic[cls][1] += 1
            else:
                cls_id = len(class_dic)
                class_dic[cls] = [cls_id, 1]
            xmlbox = obj.find('bndbox')
            bb = [xmlbox.find('xmin').text,\
                  xmlbox.find('ymin').text,\
                  xmlbox.find('xmax').text,\
                  xmlbox.find('ymax').text]
            num_obj += 1
            xmlbox = obj.find('bndbox')
            write_box += str(cls_id).ljust(4) \
                    + bb[0].ljust(6) + bb[1].ljust(6)\
                    + bb[2].ljust(6) + bb[3].ljust(6)\
                    + difficult + '\n'
        write_lines += str(num_obj) + '\n' + write_box
        in_file.close()

print 'ImageNums:', image_index + 1

out_file.writelines(write_lines)
out_file.close()

fp = open('./labels/class_index.txt', 'w')
for key in class_dic.keys():
    fp.write(key.ljust(25) + str(class_dic[key][0]) + '\n')
    print('{:25}{:5}{:5}'.format(key, class_dic[key][0], class_dic[key][1]))
fp.close()

