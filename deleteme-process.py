from vernier_capture import *
from rgb_capture import *
from thermal_capture import *
import argparse
import datetime as dt
from multiprocessing import Process

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

args = parser.parse_args()

if args.startcd > 0:
    record_start_time = dt.datetime.now() + dt.timedelta(seconds=args.startcd)
    record_start_time = record_start_time.strftime("%H:%M:%S")
else:
    record_start_time = args.rstime

selected_subject = args.subject
selected_duration = args.duration

capturingrgb = RGBCapture(
    subject_name=selected_subject,
    record_start_time=record_start_time,
    duration=selected_duration,
)
capturingthermal = PT2Capture(
    subject_name=selected_subject,
    record_start_time=record_start_time,
    duration=selected_duration,
)


def startthergb():
    capturingrgb.start_capture_rgb()


def startthethermal():
    capturingthermal.start_capture_pt()


rgb_process = Process(target=startthergb)
thermal_process = Process(target=startthethermal)
rgb_process.start()
thermal_process.start()
rgb_process.join()
thermal_process.join()
