# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
import sys
from os import listdir, getcwd
from collections import OrderedDict
from random import shuffle


def getTrainTestLists(jpegImg_Dir, xmlLabel_Dir, xmlLists):

    write_lines = []
    for rootDir, dirs, files in os.walk(xmlLabel_Dir):
        for file in files:
            xmlFile = os.path.join(rootDir, file)
            if file.split('.')[-1] != 'xml':
                print 'Error format', xmlFile
                continue
            fileName = file.split('.')[0]

            # xml and jpeg are all needed
            jpgFile = os.path.join(jpegImg_Dir, fileName + '.jpg')
            if os.path.isfile(jpgFile):
                write_lines.append(xmlFile + '\n')
            else:
                print 'missing:', jpgFile
                continue

    shuffle(write_lines)
    L = int(len(write_lines)*0.1)
    # test lists
    out_file = open('labels/%s'%(xmlLists[0]),'w')
    out_file.writelines(write_lines[:L])
    out_file.close()

    # train lists
    out_file = open('labels/%s'%(xmlLists[1]),'w')
    out_file.writelines(write_lines[L:])
    out_file.close()


def getFRCNNTrainTestDatasets(jpegImg_Dir, xmlLabel_Dir, xmlLists):
    testFileName = 'voc2007.test'
    trainValFileName = 'voc2007.trainval'
    trainTestSets = [testFileName, trainValFileName]

    class_dic = OrderedDict()
    for eachLists in xmlLists:
        fileList_fp = open('labels/%s'%(eachLists), 'r')
        i = xmlLists.index(eachLists)

        # write FRCNN train or test datasets
        out_file = open('labels/%s'%(trainTestSets[i]),'w')
        write_lines = []
        image_index = 0
        for eachline in fileList_fp.readlines():
            xmlFile = eachline.split(xmlLabel_Dir + '/')[1]
            fileName = xmlFile.split('.')[0]
            imgFile = fileName + '.jpg'
            if not os.path.isfile(os.path.join(jpegImg_Dir, imgFile)):
                print 'Error:', imgFile, 'is not exist'
                continue
            write_lines += '# ' + str(image_index) + '\n'
            image_index += 1
            eachline = eachline.strip('\n')
            in_file = open(eachline, 'r')
            tree = ET.parse(in_file)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)

            write_lines += imgFile + '\n'
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
        fileList_fp.close()

        print eachLists, 'has imageNums:', image_index
        out_file.writelines(write_lines)
        out_file.close()


    fp = open('./labels/class_index.txt', 'w')
    for key in class_dic.keys():
        fp.write(key.ljust(25) + str(class_dic[key][0]) + '\n')
        print('{:25}{:5}{:5}'.format(key, class_dic[key][0], class_dic[key][1]))
    fp.close()

if __name__ == '__main__':
    rootDir = '/apps/liusj/testLabelImgs'
    if len(sys.argv) != 2:
        print 'Usage:', sys.argv[0], 'jpgxmlRootDir'
        print 'Note: jpgxmlRootDir has JPEGImages Annotations'
        print 'Use default', rootDir
    else:
        rootDir = sys.argv[1]
    jpegImg_Dir = rootDir + '/' + 'JPEGImages'
    xmlLabel_Dir = rootDir + '/' + 'Annotations'

    xmlLists = ['testLists.txt', 'trainLists.txt']

    # 生成的label所在目录
    if not os.path.exists('labels/'):
        os.makedirs('labels/')

    getTrainTestLists(jpegImg_Dir, xmlLabel_Dir, xmlLists)
    getFRCNNTrainTestDatasets(jpegImg_Dir, xmlLabel_Dir, xmlLists)
