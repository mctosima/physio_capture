from vernier_capture import *
from rgb_capture import *
from thermal_capture import *
import argparse
import datetime as dt
import threading
from threading import Thread


def main_capture_func(
    subject, record_start_time, duration, connection_mode, save_path, vernier_fps
):
    """
    Main function to capture RGB, Thermal and Vernier data
    """
    rgb_capture = RGBCapture(subject, record_start_time, duration, save_path)

    thermal_capture = PT2Capture(subject, record_start_time, duration, save_path)

    # vernier_capture = VernierCapture(subject, record_start_time, duration, connection_mode, save_path, vernier_fps)

    def rgb_capture_thread():
        rgb_capture.start_capture_rgb()

    def thermal_capture_thread():
        thermal_capture.start_capture_thermal()

    # def vernier_capture_thread():
    #     vernier_capture.start_capture_vernier()

    rgb_thread = Thread(target=rgb_capture_thread)
    thermal_thread = Thread(target=thermal_capture_thread)
    # vernier_thread = Thread(target=vernier_capture_thread)

    # start the thread
    rgb_thread.start()
    thermal_thread.start()
    # vernier_thread.start()


if __name__ == "__main__":

    # create args parsing
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--subject",
        type=str,
        help="Subject name",
        required=True,
    )

    parser.add_argument(
        "--rstime",
        type=str,
        help="Record start time in format HH:MM:SS",
    )

    parser.add_argument(
        "--startcd",
        type=int,
        default=0,
        help="Start capture in countdown mode (seconds)",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration of the recording in seconds",
    )

    parser.add_argument(
        "--connection_mode",
        type=str,
        default="usb",
        help="Connection mode for Vernier sensors",
    )

    parser.add_argument(
        "--save_path",
        type=str,
        default="./dataset",
        help="Path to save the data",
    )

    parser.add_argument(
        "--vernier_fps",
        type=int,
        default=20,
        help="Frames per second for Vernier sensors",
    )

    parser.add_argument(
        "--runmin",
        type=bool,
        default=False,
        help="Run the capture automatically in the next minute",
    )

    args = parser.parse_args()

    if not args.runmin:
        if args.startcd > 0:
            record_start_time = dt.datetime.now() + dt.timedelta(seconds=args.startcd)
            record_start_time = record_start_time.strftime("%H:%M:%S")
        else:
            record_start_time = args.rstime

    if args.runmin:
        nowtime = dt.datetime.now()
        nowtime = nowtime.strftime("%H:%M")
        nowtime = nowtime + dt.timedelta(seconds=60)
        record_start_time = nowtime.strftime("%H:%M:%S")

    main_capture_func(
        subject=args.subject,
        record_start_time=record_start_time,
        duration=args.duration,
        connection_mode=args.connection_mode,
        save_path=args.save_path,
        vernier_fps=args.vernier_fps,
    )
