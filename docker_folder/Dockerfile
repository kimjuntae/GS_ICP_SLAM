FROM gsicp_slam


# 직접 git clone으로 저장소 가져오기
RUN echo "===== 새로운 방식으로 저장소 클론 ====="
WORKDIR /tmp
RUN git clone --recursive https://github.com/Lab-of-AI-and-Robotics/GS_ICP_SLAM.git

# 클론된 저장소에서 fast_gicp 확인
RUN echo "===== 클론된 저장소의 fast_gicp 확인 ====="
RUN ls -la /tmp/GS_ICP_SLAM/submodules/fast_gicp/ || echo "클론된 저장소에 fast_gicp가 없습니다"

# fast_gicp에서 CMakeLists.txt 확인
RUN ls -la /tmp/GS_ICP_SLAM/submodules/fast_gicp/CMakeLists.txt || echo "CMakeLists.txt 파일이 없습니다"

# 클론된 저장소에서 빌드 시도
RUN echo "===== 클론된 저장소에서 빌드 시도 ====="
WORKDIR /tmp/GS_ICP_SLAM/submodules/fast_gicp
RUN mkdir -p build
WORKDIR /tmp/GS_ICP_SLAM/submodules/fast_gicp/build
RUN cmake .. || echo "CMAKE 실패"
RUN make -j6 || echo "MAKE 실패"

WORKDIR ..
RUN python setup.py install --user

# RUN pip install submodules/diff-gaussian-rasterization
# RUN pip install submodules/simple-knn
# 빌드 결과물 복사 (선택적)
RUN echo "===== 빌드 결과물 복사 시도 ====="
RUN mkdir -p /sources/GS_ICP_SLAM/submodules/fast_gicp/build
RUN cp -r /tmp/GS_ICP_SLAM/submodules/fast_gicp/build/* /sources/GS_ICP_SLAM/submodules/fast_gicp/build/ || echo "결과물 복사 실패"

## Viewer
### Dependency
RUN sudo apt install -y libglew-dev libgtk-3-dev libassimp-dev libglfw3-dev libavdevice-dev libxxf86vm-dev
#### opencv (ver 4.5 required)
RUN sudo apt-get install -y libjpeg-dev libtiff5-dev libpng-dev \
    libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev \
    libv4l-dev v4l-utils \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    libgtk2.0-dev mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev \
    libatlas-base-dev gfortran libeigen3-dev
WORKDIR /sources
RUN mkdir opencv
WORKDIR /sources/opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.5.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.5.zip
RUN unzip opencv.zip && unzip opencv_contrib.zip
RUN rm opencv.zip && rm opencv_contrib.zip
WORKDIR /sources/opencv/opencv-4.5.5
RUN mkdir build
WORKDIR /sources/opencv/opencv-4.5.5/build
RUN cmake -D OPENCV_EXTRA_MODULES_PATH=/sources/opencv/opencv_contrib-4.5.5/modules ..
RUN make -j6
RUN sudo make install

#### embree 3.0
WORKDIR /sources
RUN wget https://github.com/embree/embree/archive/refs/tags/v3.0.0.tar.gz
RUN tar -zxvf v3.0.0.tar.gz
WORKDIR /sources/embree-3.0.0
RUN mkdir build
WORKDIR /sources/embree-3.0.0/build
RUN cmake -D EMBREE_ISPC_SUPPORT=False ..
RUN make -j6
RUN sudo make install

### build / install
# WORKDIR /sources/GS_ICP_SLAM/SIBR_viewers
# RUN cmake -Bbuild . -DCMAKE_BUILD_TYPE=Release
# RUN cmake --build build -j6 --target install# 작업 디렉토리를 프로젝트 루트로 설정
WORKDIR /sources/GS_ICP_SLAM

CMD ["/bin/bash"]