import datetime as dt
import numpy as np
import pandas as pd

captured_data = np.array([[-17,-16],[-19,-29]])
time_stamp = np.array([])
time_stamp = np.append(time_stamp, str(dt.datetime.now()))
time_stamp = np.append(time_stamp, str(dt.datetime.now()))
print(captured_data)
print(time_stamp)

# create new data frame from captured_data and time_stamp
df = pd.DataFrame(captured_data, columns = ['RR', 'ECG'])
df['time_stamp'] = time_stamp
print(df)