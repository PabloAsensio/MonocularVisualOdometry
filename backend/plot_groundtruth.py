import configparser

import pandas as pd
import matplotlib.pyplot as plt

def read_groundtruth(groundtruth_file: str, dataset: str) -> list:

    if dataset == "vkitti2":
        df = pd.read_csv(groundtruth_file, sep=" ")
        return df[df["cameraID"] == 0].copy()

    with open(groundtruth_file, "r") as f:
        return f.readlines()


def get_groundtruth(file: str, dataset: str):
    
    if dataset == "kitti":
        df = pd.read_csv(file, sep=" ", usecols=[3, 7, 11], names=["x", "y", "z"], header=None)
        return df.copy()

    if dataset == "vkitti2":
        df = pd.read_csv(file, sep=" ", usecols=[1, 5, 9, 13], names=["cameraID" ,"x", "y", "z"], header=0)
        return df[df["cameraID"] == 0].copy()

    if dataset == "euromav":
        df = pd.read_csv(file, sep=",", usecols=[1, 2, 3], names=["x", "y", "z"], header=0)
        return df.copy()
    
    print('Dataset not supported'.upper())
    exit(0)


def plot_groundtruth(gt, dataset: str):
    plt.plot(gt['x'], gt['z'])
    plt.title(dataset.upper())
    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()

def plot_groundtruth3D(gt, dataset: str):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    ax.plot3D(gt['x'], gt['y'], gt['z'])
    plt.title(dataset.upper())
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read('../dataset.cfg')
    dataset_info = dict(config.items('TO_READ'))

    gt = get_groundtruth(dataset_info['ground_truth_file'], dataset_info['dataset'])
    print(dataset_info['dataset'])
    print(gt)
    plot_groundtruth(gt, dataset_info['dataset'])
    # plot_groundtruth3D(gt, dataset_info['dataset'])