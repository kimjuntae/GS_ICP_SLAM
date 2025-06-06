#!/bin/bash

# DISPLAY 설정
export DISPLAY=$(ip route | grep default | awk '{print $3}'):0.0

# Docker 실행
docker run -it \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  -e USER=jtkim \
  --runtime=nvidia \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -v /home/jtkim/sources/GS_ICP_SLAM:/sources/GS_ICP_SLAM \
  --shm-size=12g \
  --net host \
  --gpus all \
  --privileged \
  --name gsicpslam \
  gsicp_slam_img:latest /bin/bash