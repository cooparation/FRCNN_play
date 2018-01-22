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

BUILD=./build/examples/FRCNN/demo_frcnn_api.bin
ModelFile=./zf/test.prototxt
CaffeModel=models/FRCNN/zf_faster_rcnn_final.caffemodel
ConfigFile=./zf/voc_config.json

ImageRootDir=./images/

OutputDir=output/FRCNN/results/

$BUILD --gpu $gpu \
       --model $ModelFile \
       --weights $CaffeModel \
       --default_c $ConfigFile \
       --image_dir $ImageRootDir  \
       --out_dir $OutputDir
