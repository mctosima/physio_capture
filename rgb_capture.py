import datetime as dt
import numpy as np
import cv2
import os
import argparse


class RGBCapture:
    """
    Capturing RGB images from camera
    """

    def __init__(
        self,
        subject_name,
        record_start_time,
        device_id=1,
        save_path="./dataset",
        duration=10,
    ):

        cap = cv2.VideoCapture(
            device_id, cv2.CAP_DSHOW
        )  # windowsOS needs cv2.CAP_DSHOW
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)

        if not cap.isOpened():
            print("RGB Camera not found!")
            exit(1)

        self.cap = cap
        self.save_path = save_path
        self.duration = duration
        self.subject_name = subject_name
        self.record_start_time = dt.datetime.combine(
            dt.date.today(), dt.datetime.strptime(record_start_time, "%H:%M:%S").time()
        )

        # check if time is in the past
        if self.record_start_time - dt.timedelta(seconds=4) < dt.datetime.now():
            raise ValueError(
                "Start time is in the past. Please enter a valid start time."
            )

        self.record_end_time = self.record_start_time + dt.timedelta(
            seconds=self.duration
        )

        if not os.path.exists(self.save_path + "/" + self.subject_name + "/rgb"):
            os.makedirs(self.save_path + "/" + self.subject_name + "/rgb")
            print("Created folder for RGB images")

    def start_capture_rgb(self):
        """
        Capturing RGB images from camera
        """

        cnt = 0
        frame_no = 0

        while dt.datetime.now() <= self.record_start_time - dt.timedelta(seconds=3):
            if cnt == 0:
                print(
                    f"[RGBCAPTURE] -> Waiting for start time {self.record_start_time.strftime('%H:%M:%S')}..."
                )
                print(f"Time Remaining: {self.record_start_time - dt.datetime.now()}")
                cnt += 1

        print(f"Capturing RGB Images... (-3 seconds)")
        cv2.namedWindow("PreviewRGB", cv2.WINDOW_NORMAL)
        while True:
            ret, img = self.cap.read()

            if ret == False:
                raise Exception("Error reading image")
            cv2.imshow("PreviewRGB", img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            if (
                dt.datetime.now() <= self.record_end_time
                and dt.datetime.now() >= self.record_start_time
            ):
                filename = (
                    f"{frame_no}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                )
                cv2.imwrite(
                    f"{self.save_path}/{self.subject_name}/rgb/{filename}",
                    img,
                )
                frame_no += 1

            if dt.datetime.now() > self.record_end_time:
                break

        cv2.destroyAllWindows()


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
        help="Start time of recording in HH:MM:SS format",
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Duration of recording in seconds",
        default=60,
    )
    parser.add_argument(
        "--device",
        type=int,
        help="Device ID of the camera",
        default=2,
    )

    args = parser.parse_args()
    RGBCapture(
        args.name, args.stime, duration=args.duration, device_id=args.device
    ).start_capture_rgb()

    # subject_name = "alice"
    # # record_start_time = "11:15:00"

    # # for development only
    # record_start_time = (dt.datetime.now() + dt.timedelta(seconds=8)).strftime(
    #     "%H:%M:%S"
    # )

    # print(record_start_time)

    # duration = 10

    # rgb_capture = RGBCapture(
    #     subject_name,
    #     record_start_time,
    #     duration=duration,
    # )

    # rgb_capture.start_capture_rgb()
