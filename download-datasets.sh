#!/bin/bash

EUROCMAV_COMMON="http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/"
EUROCMAV_LIST=("machine_hall/MH_01_easy/MH_01_easy.zip"
    "machine_hall/MH_02_easy/MH_02_easy.zip"
    "vicon_room1/V1_01_easy/V1_01_easy.zip"
    "vicon_room2/V2_01_easy/V2_01_easy.zip")

# Download EUROCMAV dataset
cd ~ || exit 1
mkdir -p datasets/eurocmav && cd datasets/eurocmav || exit

# Download zips
for RELATIVE_PATH in "${EUROCMAV_LIST[@]}"; do
    DOWNLOAD_LINK="${EUROCMAV_COMMON}${RELATIVE_PATH}"
    wget "${DOWNLOAD_LINK}"
done

# Unzip
for ZIP in *.zip; do
    # Create folder and move zip on it
    FOLDER=$(echo "${ZIP}" | awk '{split($0,name,"."); print name[1]}')
    mkdir "${FOLDER}"
    mv "${ZIP}" "${FOLDER}"
    cd "${FOLDER}" || exit
    unzip "${ZIP}" >/dev/null 2>/dev/null
    # Delete zip
    rm -f "${ZIP}"
    cd ..
done

# Download KITTI dataset
cd ~ || exit 1
mkdir -p datasets/kitti && cd datasets/kitti || exit
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_gray.zip
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_poses.zip
unzip data_odometry_gray.zip >/dev/null 2>/dev/null
unzip data_odometry_poses.zip >/dev/null 2>/dev/null
rm -rf ./*.zip

# Download VKITTI2 dataset
cd ~ || exit 1
mkdir -p datasets/vkitti2/rgb && cd datasets/vkitti2/rgb || exit
wget http://download.europe.naverlabs.com//virtual_kitti_2.0.3/vkitti_2.0.3_rgb.tar
tar -xvf vkitti_2.0.3_rgb.tar >/dev/null 2>/dev/null
rm -f vkitti_2.0.3_rgb.tar
cd ..
mkdir gt && cd gt || exit
wget http://download.europe.naverlabs.com//virtual_kitti_2.0.3/vkitti_2.0.3_textgt.tar.gz
tar -xvf vkitti_2.0.3_textgt.tar.gz >/dev/null 2>/dev/null
rm -f vkitti_2.0.3_textgt.tar.gz
