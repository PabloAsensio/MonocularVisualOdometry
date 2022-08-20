#!/bin/bash

EUROCMAV_COMMON="http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/"
EUROCMAV_LIST=( "machine_hall/MH_01_easy/MH_01_easy.zip"
                "machine_hall/MH_02_easy/MH_02_easy.zip"
                "vicon_room1/V1_01_easy/V1_01_easy.zip"
                "vicon_room2/V2_01_easy/V2_01_easy.zip")

# Download EUROCMAV dataset 
cd ~ || exit 1
mkdir -p datasets/eurocmav && cd datasets/eurocmav || exit

# Download zips
for RELATIVE_PATH in "${EUROCMAV_LIST[@]}"
do
   DOWNLOAD_LINK="${EUROCMAV_COMMON}${RELATIVE_PATH}"
   wget "${DOWNLOAD_LINK}" 
done

# Unzip
for ZIP in *.zip
do
    # Create folder and move zip on it
    FOLDER=$(echo "${ZIP}" | awk '{split($0,name,"."); print name[1]}')
    mkdir "${FOLDER}" 
    mv "${ZIP}" "${FOLDER}" 
    cd "${FOLDER}" || exit 
    tar -xzf "${ZIP}"
    # Delete zip
    rm -f "${ZIP}"
    cd ..
done
