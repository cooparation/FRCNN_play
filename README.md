**Special Feature for This Caffe Repository**

- Clone from the official caffe, will continuely be up-to-date by the official caffe code
- Faster rcnn joint train, test and evaluate
- Action recognition (Two Stream CNN)

### Demo
Using `sh examples/FRCNN/demo_frcnn.sh`, the will process five pictures in the `examples/FRCNN/images`, and put results into `examples/FRCNN/results`.

Note: You should prepare the trained caffemodel into `models/FRCNN`, such as `ZF_faster_rcnn_final.caffemodel` for ZF model.

### Prepare for training and evaluation
Get the training and test dataLists `tools/1_convert_xml2FRCNNTrainDatasets.py`

The training data list is `examples/FRCNN/dataset/voc2007.trainval`.

The testing data list is `examples/FRCNN/dataset/voc2007.trainval`.

Create symlinks for the PASCAL VOC dataset `ln -s $YOUR_VOCdevkit_Path $CAFFE_ROOT/VOCdevkit`.

As shown in VGG example `models/FRCNN/vgg16/train_val.proto`, the original pictures should appear at `$CAFFE_ROOT/VOCdevkit/VOC2007/JPEGImages/`. (Check window\_data\_param in FrcnnRoiData)

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
`sh examples/FRCNN/zf/train_frcnn.sh` will start training process of voc2007 data using ZF model.

If you use the provided training script, please make sure:
- VOCdevkit is within $CAFFE\_ROOT and VOC2007 in within VOCdevkit
- ZF pretrain model should be put into models/FRCNN/ as ZF.v2.caffemodel

`examples/FRCNN/convert_model.py` transform the parameters of `bbox_pred` layer by mean and stds values,
because the regression value is normalized during training and we should recover it to obtain the final model.

### Evaluation
`sh examples/FRCNN/zf/test_frcnn.sh` the will evaluate the performance of voc2007 test data using the trained ZF model.

- First Step of This Shell : Test all voc-2007-test images and output results in a text file.
- Second Step of This Shell : Compare the results with the ground truth file and calculate the mAP.

### Detail

Shells and prototxts for different models are listed in the `examples/FRCNN` and `models/FRCNN`

More details in the code:
- `include/api/FRCNN` and `src/api/FRCNN` for demo and test api
- `include/caffe/FRCNN` and `src/caffe/FRCNN` contains all codes related to Faster R-CNN

### Commands, Rebase From Caffe Master
- git clone https://github.com/cooparation/caffe-faster-rcnn.git
- git checkout dev
- git checkout ef466f43e5da3d68cae5892078f63cd4c6f4db5b
- compile the Caffe
- numpy(1.13.3)

## QA
- CUB not found, when compile for GPU version, `frcnn_proposal_layer.cu` requires a head file `<cub/cub.cuh>`. CUB is library contained in the official Cuda Toolkit, usually can be found in ` /usr/local/cuda/include/thrust/system/cuda/detail/`. You should add this path in your `Makefile.config` (try `locate ''cub.cuh''` to find cub on your system)
- When Get `error: RPC failed; result=22, HTTP code = 0`, use `git config http.postBuffer 524288000`, increases git buffer to 500mb
- When Get collections import error, it often comes from the conflict bettewn matplotlib and python2.7, what you could do is just to remove the matplotlib/collections.py

## Two-Stream Convolutional Networks for Action Recognition in Video

See codes `src/caffe/ACTION_REC` and `include/caffe/ACTION_REC`

