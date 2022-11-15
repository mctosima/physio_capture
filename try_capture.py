from datetime import datetime
from time import sleep

try:
    import cv2
except ImportError:
    print ("ERROR python-opencv must be installed")
    exit(1)

class OpenCvCapture(object):
    """
    Encapsulate state for capture from Pure Thermal 1 with OpenCV
    """

    def __init__(self):
        # capture from the LAST camera in the system
        # presumably, if the system has a built-in webcam it will be the first
        cv2_cap = cv2.VideoCapture(0)
        cv2_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        cv2_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        cv2_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
        cv2_cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        # cv2_cap.set(cv2.CAP_PROP_FPS, 12.0)


        if not cv2_cap.isOpened():
            print ("Camera not found!")
            exit(1)

        self.cv2_cap = cv2_cap

    def show_video(self):
        """
        Run loop for cv2 capture from lepton
        """

        cv2.namedWindow("lepton", cv2.WINDOW_NORMAL)
        print ("Running, ESC or Ctrl-c to exit...")
        cnt = 1

        start_time = datetime.now()

        # run for 10 seconds
        while (datetime.now() - start_time).seconds <= 10:
            ret, img = self.cv2_cap.read()
            print(f"Frame: {cnt}")
            print(img.shape)
            cnt += 1

            if ret == False:
                print ("Error reading image")
                break

            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            # img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
            cv2.imshow("lepton", img)
            
            # wait for ESC key to exit
            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    OpenCvCapture().show_video()