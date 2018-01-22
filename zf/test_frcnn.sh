#!/usr/bin/env sh
# This script test four voc images using faster rcnn end-to-end trained model (ZF-Model)
# determine whether $1 is empty
if [ ! -n "$1" ] ;then
    echo "$1 is empty, default is 0"
    gpu=0
else
    echo "use $1-th gpu"
    gpu=$1
fi

pid=$$

BUILD=./build/examples/FRCNN/test_frcnn.bin

ModelFile=./zf/test.prototxt
CaffeModel=models/FRCNN/zf_faster_rcnn_final.caffemodel
ConfigFile=./zf/voc_config.json

ImageRootDir=/apps/liusj/datasets/DetectionFoodDatasets/JPEGImages/
GRImageLists=./labels/det.test

#GetObjectImageList=output/FRCNN/results/test_zf_${pid}.frcnn

GetObjectImageList=output/FRCNN/results/test_zf.frcnn

$BUILD --gpu $gpu \
    --model $ModelFile \
    --weights $CaffeModel \
    --default_c $ConfigFile \
    --image_root $ImageRootDir \
    --image_list $GRImageLists \
    --out_file $GetObjectImageLists \
    --max_per_image 100

CAL_AP=examples/FRCNN/calculate_voc_ap.py

python $CAL_AP --gt $GRImageLists \
    --answer $GetObjectImageLists \
    --overlap 0.5
