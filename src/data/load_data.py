import pandas as pd

def load_data(path):
    df = pd.read_csv(path, sep=',')
    df.info()
    return df
