from dataclasses import replace


def read_kitti(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "").split(" ")
        return lines
