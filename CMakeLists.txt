cmake_minimum_required(VERSION 2.8.12)
project(frcnn_play)

option(CPU_ONLY "If use cpu only" OFF)

# set caffe root dir
set(Caffe_DIR ${PROJECT_SOURCE_DIR}/../caffe-faster-rcnn/.build_release)
find_package(Caffe)
include_directories(${Caffe_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/include)

add_subdirectory(${PROJECT_SOURCE_DIR}/src/api/FRCNN)
add_subdirectory(${PROJECT_SOURCE_DIR}/examples)
