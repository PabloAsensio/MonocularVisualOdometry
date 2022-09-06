import pandas as pd

def read_eurocmav_timestamp_groundtruth(path: str) -> list:
    df = pd.read_csv(path, delimiter=',', header=0)
    timestamps = df['#timestamp']
    return timestamps.to_list()
