from gdx import gdx
import datetime as dt
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import argparse


class VernierCapture:
    """
    Capturing RR and ECG from Vernier Go Direct Sensors and save it to CSV files
    Args:
        subject_name (str): Name of the subject
        record_start_time (str): Start time of the recording in the format of "HH:MM:SS"
        save_path (str): Path to save the data, default: "./dataset"
        duration (int): Duration of the recording in seconds, default: 10
        fps (int): Frames per second, default: 20 (currently only support 20 for the RR)
    """

    def __init__(
        self,
        subject_name,
        record_start_time,
        save_path="./dataset",
        duration=10,
        fps=20,
        connection_mode="ble",
    ):

        self.save_path = save_path
        self.duration = duration
        self.subject_name = subject_name
        self.record_start_time = dt.datetime.combine(
            dt.date.today(), dt.datetime.strptime(record_start_time, "%H:%M:%S").time()
        )

        # check if start_time is in the past -> Raise Error
        if self.record_start_time - dt.timedelta(seconds=4) < dt.datetime.now():
            raise ValueError(
                "Start time is in the past. Please enter a valid start time."
            )

        # count the end time
        self.record_end_time = self.record_start_time + dt.timedelta(
            seconds=self.duration
        )

        period = 1000/fps  # in ms

        try:
            gdx.open(
                connection=connection_mode,
                device_to_open="GDX-RB 0K1002H6, GDX-EKG 0U1000S2",
            )
            gdx.select_sensors([[1], [1,2]])
            gdx.start(period)
        except:
            gdx.stop()
            gdx.close()

        self.column_headers = gdx.enabled_sensor_info()
        self.gdx = gdx

        # check if the directory exists
        if not os.path.exists(self.save_path + "/" + self.subject_name + "/vernier"):
            os.makedirs(self.save_path + "/" + self.subject_name + "/vernier")
            print(
                f"Created directory {self.save_path + '/' + self.subject_name + '/vernier'}"
            )

    def start_capture_vernier(self):
        """
        Start capturing RR and ECG from Vernier Go Direct Sensors
        """
        cnt = 0
        captured_data = []
        while dt.datetime.now() <= self.record_start_time - dt.timedelta(seconds=3):
            if cnt == 0:
                print(f"[VERNIER] -> Waiting for the start time at {self.record_start_time}...")
                print(f"Time Remaining: {self.record_start_time - dt.datetime.now()}")
                cnt += 1

        print("Capturing the data... (-3 Seconds)")
        # We need to do this because everytime the gdx.read() called, it flows with huge amount of data.

        while True:
            measurements = self.gdx.read()

            if (
                dt.datetime.now() <= self.record_end_time
                and dt.datetime.now() >= self.record_start_time
            ):
                measurement_combine = (
                    dt.datetime.now(),
                    measurements[0],
                    measurements[1],
                    measurements[2],
                )
                captured_data.append(measurement_combine)

            if dt.datetime.now() > self.record_end_time:
                break

        # save the data to CSV
        csv_name = (
            self.save_path
            + "/"
            + self.subject_name
            + "/vernier/"
            + self.subject_name
            + "_vernier.csv"
        )
        np.savetxt(csv_name, captured_data, delimiter=",", fmt="%s, %.20f, %.20f, %.20f")

        print(
            f"Captured data saved to {self.save_path}/{self.subject_name}/vernier/{self.subject_name}_vernier.csv"
        )

        self.gdx.stop()
        self.gdx.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        type=str,
        help="Name of the subject",
    )
    parser.add_argument(
        "--stime",
        type=str,
        help="Start time of the recording in the format of 'HH:MM:SS'",
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Duration of the recording in seconds",
        default=60,
    )
    parser.add_argument(
        "--fps",
        type=int,
        help="Frames per second",
        default=20,
    )
    parser.add_argument(
        "--conn",
        type=str,
        help="Connection mode",
        default="usb",
    )
    args = parser.parse_args()
    gdx = gdx.gdx()
    VernierCapture(
        subject_name=args.name,
        record_start_time=args.stime,
        duration=args.duration,
        fps=args.fps,
        connection_mode=args.conn,
    ).start_capture_vernier()

    # gdx = gdx.gdx()
    # subject_name = "bob"
    # # record_start_time = "11:11:00"

    # # for development purpose
    # record_start_time = dt.datetime.now() + dt.timedelta(seconds=8)
    # record_start_time = record_start_time.strftime("%H:%M:%S")

    # save_path = "./dataset"
    # duration = 10
    # fps = 20 # bluetooth max 20

    # vc = VernierCapture(
    #     subject_name,
    #     record_start_time,
    #     save_path,
    #     duration,
    #     fps,
    #     connection_mode="usb",
    # )

    # vc.start_capture_vernier()

    # VernierCapture.integrity_check(
    #     "dataset/alice/vernier/alice_vernier.csv"
    # )
