import datetime as dt
import numpy as np
import cv2
import os


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
        cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT, 2560
        )  # strange, when set to 2k, in become 720p
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
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

        while dt.datetime.now() <= self.record_start_time - dt.timedelta(seconds=3):
            if cnt == 0:
                print(
                    f"Waiting for start time {self.record_start_time.strftime('%H:%M:%S')}..."
                )
                print(f"Time Remaining: {self.record_start_time - dt.datetime.now()}")
                cnt += 1

        print(f"Capturing RGB Images... (-3 seconds)")
        cv2.namedWindow("PreviewRGB", cv2.WINDOW_NORMAL)
        while True:
            ret, img = self.cap.read()
            print(img.shape)
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
                cv2.imwrite(
                    f"{self.save_path}/{self.subject_name}/rgb/{dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg",
                    img,
                )

            if dt.datetime.now() > self.record_end_time:
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    subject_name = "test"
    # record_start_time = "11:15:00"

    # for development only
    record_start_time = dt.datetime.now() + dt.timedelta(seconds=8)
    record_start_time = record_start_time.strftime("%H:%M:%S")
    duration = 10

    rgb_capture = RGBCapture(
        subject_name,
        record_start_time,
        duration=duration,
    )

    rgb_capture.start_capture_rgb()
