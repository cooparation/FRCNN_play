# Faster RCNN c++ with caffe

**Special Feature for This Caffe Repository**

- Clone from the official caffe, will continuely be up-to-date by the official caffe code
- Faster rcnn joint train, test and evaluate
- Action recognition (Two Stream CNN)

### Deps
- git clone https://github.com/cooparation/caffe-faster-rcnn.git
- git checkout dev
- git checkout ef466f43e5da3d68cae5892078f63cd4c6f4db5b
- compile the Caffe
- numpy(1.13.3)
- cd FRCNN_play_ROOT and create the softlink `caffe` with Caffe Master

### Demo
Using `sh zf/demo_frcnn.sh`, the will process five pictures in the `examples/FRCNN/images`, and put results into `output/FRCNN/results`.

Note: You should prepare the trained caffemodel into `models/FRCNN`, such as `ZF_faster_rcnn_final.caffemodel` for ZF model.

### Prepare for training and evaluation
Get the training and test dataLists `tools/1_convert_xml2FRCNNTrainDatasets.py`

The training data list is `examples/FRCNN/dataset/voc2007.trainval`.

The testing data list is `examples/FRCNN/dataset/voc2007.trainval`.

If you want to train Faster R-CNN on your own dataset, you may prepare custom dataset list.
The format is as below
```
# image-id
image-name
number of boxes
label x1 y1 x2 y2 difficulty
...
```

### Training
`sh ./zf/train_frcnn.sh` will start training process

If you use the provided training script, please make sure:
- ZF pretrain model should be put into models/FRCNN/ as ZF.v2.caffemodel

`examples/FRCNN/convert_model.py` transform the parameters of `bbox_pred` layer by mean and stds values,
because the regression value is normalized during training and we should recover it to obtain the final model.

### Evaluation
`sh ./zf/test_frcnn.sh` the will evaluate the performance of voc2007 test data using the trained ZF model.

- First Step of This Shell : Test all voc-2007-test images and output results in a text file.
- Second Step of This Shell : Compare the results with the ground truth file and calculate the mAP.

### Detail

Shells and prototxts for different models are listed in the `examples/FRCNN` and `models/FRCNN`

## QA
- When Get collections import error, it often comes from the conflict bettewn matplotlib and python2.7, what you could do is just to remove the matplotlib/collections.py or rename it

## Two-Stream Convolutional Networks for Action Recognition in Video

See codes `caffe-faster-rcnn/src/caffe/ACTION_REC` and `caffe-faster-rcnn/include/caffe/ACTION_REC`
## Acknowlegement
I greatly thank [D-X-Y](https://github.com/D-X-Y/caffe-faster-rcnn)
And I would like to thank all the authors of every network
