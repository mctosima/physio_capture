import datetime as dt
import numpy as np
import cv2
import os


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

    def start_capture_pt(self):

        cv2.namedWindow("PreviewThermal", cv2.WINDOW_NORMAL)
        cnt = 0

        start_time = dt.datetime.now()
        end_time = start_time + dt.timedelta(seconds=self.duration)

        print(f"Capturing thermal images for {self.duration} seconds...")
        while dt.datetime.now() <= end_time:
            ret, img = self.cap.read()

            if ret == False:
                raise Exception("Error reading image")

            frame_numpy = np.array(img)

            # get filename from count + timestamp
            filename = f"{cnt}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            # filename = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

            # check if folder exists
            if not os.path.exists(
                self.save_path + "/" + self.subject_name + "/thermal"
            ):
                os.makedirs(self.save_path + "/" + self.subject_name + "/thermal")

            # dump to CSV
            np.savetxt(  # TODO: Create if not exist
                f"{self.save_path}/{self.subject_name}/thermal/{filename}",
                frame_numpy,
                delimiter=",",
                fmt="%d",
            )

            if (
                cnt == 1
            ):  # only run once to define the end time based on first frame read
                start_time = dt.datetime.now()
                end_time = start_time + dt.timedelta(seconds=self.duration)

            # print(f"Frame No: {cnt} | Time Now: {dt.datetime.now()}")

            cnt += 1

            # preview
            img_8bit = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            cv2.imshow("PreviewThermal", img_8bit)

            if cv2.waitKey(1) == 27:
                break

        end_time = dt.datetime.now()

        # generate report to txt
        with open(f"{self.save_path}/{self.subject_name}/report.txt", "w") as f:

            f.write(f"THERMAL DATA CAPTURE REPORT\n")
            f.write(f"Subject Name: {self.subject_name}\n")
            f.write(f"Start Time: {start_time}\n")
            f.write(f"End Time: {end_time}\n")
            f.write(f"Duration: {end_time - start_time}\n")
            f.write(f"Total Frame Count: {cnt+1}\n\n")

        print(f"Capturing done. Total frame count: {cnt+1}")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    capture = PT2Capture(
        device_id=1, save_path="./dataset", duration=10, subject_name="SampleSubject"
    )
    capture.start_capture_pt()
