import datetime as dt
import numpy as np
import cv2
import os
import argparse


class PT2Capture:
    """
    Capturing from PureThermal2 and save it to CSV
    Args:
        subject_name (str): Name of the subject
        device_id (int): Device ID of the camera
        save_path (str): Directory of Dataset
        duration (int): Duration of capturing in seconds
    """

    def __init__(
        self,
        subject_name,
        record_start_time,
        device_id=0,
        save_path="./dataset",
        duration=10,
    ):
        cap = cv2.VideoCapture(
            device_id, cv2.CAP_DSHOW
        )  # windowsOS needs cv2.CAP_DSHOW
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("Y", "1", "6", " "))
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        if not cap.isOpened():
            print("Thermal Camera not found!")
            exit(1)

        self.cap = cap
        self.save_path = save_path
        self.duration = duration
        self.subject_name = subject_name
        self.record_start_time = dt.datetime.combine(
            dt.date.today(), dt.datetime.strptime(record_start_time, "%H:%M:%S").time()
        )

        if self.record_start_time - dt.timedelta(seconds=4) < dt.datetime.now():
            raise ValueError(
                "Start time is in the past. Please enter a valid start time."
            )

        self.record_end_time = self.record_start_time + dt.timedelta(
            seconds=self.duration
        )

        if not os.path.exists(self.save_path + "/" + self.subject_name + "/thermal"):
            os.makedirs(self.save_path + "/" + self.subject_name + "/thermal")
            print("Created folder for Thermal images")

    def start_capture_pt(self):
        cnt = 0
        frame_no = 0

        while dt.datetime.now() <= self.record_start_time - dt.timedelta(seconds=3):
            if cnt == 0:
                print(
                    f"[THERMALCAPTURE] -> Waiting for start time {self.record_start_time.strftime('%H:%M:%S')}..."
                )
                print(f"Time Remaining: {self.record_start_time - dt.datetime.now()}")
                cnt += 1

        print(f"Capturing Thermal Images... (-3 seconds)")
        cv2.namedWindow("PreviewThermal", cv2.WINDOW_NORMAL)

        while True:
            # start reading frames
            ret, img = self.cap.read()
            if ret == False:
                raise Exception("Error reading image")

            img_8bit = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            cv2.imshow("PreviewThermal", img_8bit)

            # break when q is pressed
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            if (
                dt.datetime.now() <= self.record_end_time
                and dt.datetime.now() >= self.record_start_time
            ):
                frame_numpy = np.array(img)

                # get filename from count + timestamp
                filename = (
                    f"{frame_no}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.csv"
                )

                # dump to CSV
                np.savetxt(
                    f"{self.save_path}/{self.subject_name}/thermal/{filename}",
                    frame_numpy,
                    delimiter=",",
                    fmt="%d",
                )

                frame_no += 1

            if dt.datetime.now() > self.record_end_time:
                break

        cv2.destroyAllWindows()
        end_time = dt.datetime.now()


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
    PT2Capture(
        subject_name=args.name,
        record_start_time=args.stime,
        device_id=args.device,
        duration=args.duration,
    ).start_capture_pt()

    # subject_name = "alice"
    # # record_start_time = "10:00:00"

    # # for development only
    # record_start_time = (dt.datetime.now() + dt.timedelta(seconds=8)).strftime(
    #     "%H:%M:%S"
    # )
    # duration = 10
    # pt2 = PT2Capture(subject_name, record_start_time, duration=duration)
    # pt2.start_capture_pt()
