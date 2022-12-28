import time
import csv
import numpy as np
import pandas as pd
import datetime as dt
from gdx import gdx

connection_mode = "usb"
fps = 400
period = 1000/fps
duration = 15

gdx = gdx.gdx()


gdx.open(connection=connection_mode, device_to_open="GDX-EKG 0U1000S2")
gdx.select_sensors([[1]])
gdx.start(period)

# create empty array for appending data
captured_data = []
cnt = 0

# set record start time
delta_second = 8
record_start_time = dt.datetime.now() + dt.timedelta(seconds=delta_second)

# floor to the nearest second
record_start_time = record_start_time.replace(microsecond=0)

# print record_start_time until the milisecond
print(f"Start recording at {record_start_time}")

# set end time
record_end_time = record_start_time + dt.timedelta(seconds=duration)
print(f"End recording at {record_end_time} (duration: {duration} seconds)")

# create a trap for waiting
while dt.datetime.now() < record_start_time - dt.timedelta(seconds=3):
    if cnt == 0:
        print(f"Waiting for {delta_second} seconds..")
        cnt += 1

while True:
    measurements = gdx.read()

    if (dt.datetime.now() <= record_end_time and dt.datetime.now() >= record_start_time):    
        if cnt == 1:
            print(f"Capturing the data..")
            cnt += 1
        
        measurement_combine = (
            dt.datetime.now(),
            measurements[0],
        )
        captured_data.append(measurement_combine)

    if dt.datetime.now() > record_end_time:
        break

# stop and close the connection
gdx.stop()
gdx.close()

# save the data to CSV
csv_name = "ecg_data.csv"

np.savetxt(csv_name, captured_data, delimiter=",", fmt="%s")

