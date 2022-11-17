from gdx import gdx
import datetime as dt
import numpy as np
import os
import pandas as pd

class VernierCapture():
    """
    Capturing RR and ECG from Vernier Go Direct Sensors and save it to CSV files
    """

    def __init__(
        self,
        subject_name,
        record_start_time,
        save_path = "./dataset",
        duration = 10,
        fps = 40,
    ):

        self.save_path = save_path
        self.duration = duration
        self.subject_name = subject_name
        self.record_start_time = dt.datetime.combine(dt.date.today(), dt.datetime.strptime(record_start_time, "%H:%M:%S").time())

        # count the end time
        self.record_end_time = self.record_start_time + dt.timedelta(seconds=self.duration)

        period = 1/fps * 1000 # in ms

        # configure the gdX device
        
        gdx.open(connection='ble', device_to_open='GDX-RB 0K1002H6, GDX-EKG 0U1000S2')
        gdx.select_sensors([[1],[1]])
        gdx.start(period)
        self.column_headers = gdx.enabled_sensor_info()
        self.gdx = gdx

        # check if the directory exists
        if not os.path.exists(self.save_path + "/" + self.subject_name + "/vernier"):
            os.makedirs(self.save_path + "/" + self.subject_name + "/vernier")
            print(f"Created directory {self.save_path + '/' + self.subject_name + '/vernier'}")

    def start_capture_vernier(self):
        """
        Start capturing RR and ECG from Vernier Go Direct Sensors
        """
        # get current time
        cnt = 0
        captured_data = []
        while(dt.datetime.now() < self.record_start_time):
            if cnt == 0:
                print(f"Waiting for the start time at {self.record_start_time}...")
                cnt += 1

        while(dt.datetime.now() < self.record_end_time):
            measurements = self.gdx.read()
            if measurements == None:
                break
            
            print(measurements)
            time_stamp = dt.datetime.now()
            measurement_combine = (time_stamp, measurements[0], measurements[1])
            # reformat the measurements with timestamp
            
            captured_data.append(measurement_combine)


        # save the data to CSV
        csv_name = self.save_path + "/" + self.subject_name + "/vernier/" + self.subject_name + "_vernier.csv"
        np.savetxt(csv_name, captured_data, delimiter=",", fmt="%s, %.20f, %.20f")
        
        print(f"Captured data saved to {self.save_path}/{self.subject_name}/vernier/{self.subject_name}_vernier.csv")

        self.gdx.stop()
        self.gdx.close()

if __name__ == "__main__":
    gdx = gdx.gdx()
    subject_name = "jessica"
    record_start_time = "17:19:00"
    save_path = "./dataset"
    duration = 10
    fps = 40

    vc = VernierCapture(
        subject_name,
        record_start_time,
        save_path,
        duration,
        fps
    )

    vc.start_capture_vernier()