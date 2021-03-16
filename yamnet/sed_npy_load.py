import time
import numpy as np
import pandas as pd
df = pd.DataFrame(columns=['Timestamp', 'Scores'])
with open('sed.npy', 'rb') as f:
    load = np.load(f)
    df.loc[len(df)] = [time.ctime(load[0]).split()[3], load[1:]]
    while True:
        try:
            load = np.load(f)
            df.loc[len(df)] = [time.ctime(load[0]).split()[3], load[1:]]
        except:
            break
print(df)