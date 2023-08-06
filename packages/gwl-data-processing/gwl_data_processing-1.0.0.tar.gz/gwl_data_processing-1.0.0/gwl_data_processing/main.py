import numpy as np
import pandas as pd
data = pd.read_excel('Lesson3.xlsx')
df = pd.DataFrame(data)
def data_processing(df):
    data_mean = df.mean()
if __name__ == '__main__':
    data_processing(data)