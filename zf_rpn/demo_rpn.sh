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

BUILD=./build/examples/FRCNN/demo_rpn

ModelFile=./zf_rpn/test.prototxt
CaffeModel=output/FRCNN/models/zf_rpn_final.caffemodel
ConfigFile=./zf_rpn/voc_config.json

ImageRootDir=/apps/liusj/datasets/DetectionFoodDatasets/JPEGImages/

ImageList=./labels/det.test

OutFile=output/FRCNN/results/voc_test_results.rpn
OutDir=output/FRCNN/results/
if [ ! -f "$OutFile" ]; then
    touch "$OutFile"
fi

time $BUILD --gpu $gpu \
    --model $ModelFile \
    --weights $CaffeModel \
    --default_c $ConfigFile \
    --image_root $ImageRootDir \
    --image_list $ImageList \
    --out_file $OutFile \
    --out_dir $OutDir

CAL_RECALL=examples/FRCNN/calculate_recall.py

time python $CAL_RECALL --gt $ImageList \
    --answer $OutFile \
    --overlap 0.5
