import yaml


def read_euromav(file_path):
    with open(file_path, "r") as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    return data
