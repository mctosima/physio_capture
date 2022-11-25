import argparse
import subprocess
import datetime as dt
from pygrabber.dshow_graph import FilterGraph


def runcapture(
    subject_name,
    record_start_time,
    duration,
    device_id_thermal,
    device_id_rgb,
    connection_mode,
    dps,
):

    # list of subprocesses
    subprocess.Popen(
        f"start python rgb_capture.py --name {subject_name} --stime {record_start_time} --duration {duration} --device {device_id_rgb}",
        shell=True,
    )
    subprocess.Popen(
        f"start python thermal_capture.py --name {subject_name} --stime {record_start_time} --duration {duration} --device {device_id_thermal}",
        shell=True,
    )
    subprocess.Popen(
        f"start python vernier_capture.py --name {subject_name} --stime {record_start_time} --duration {duration} --conn {connection_mode} --fps {dps}",
        shell=True,
    )


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
        "--cdown",
        type=int,
        help="Countdown in seconds",
        default=10,
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Duration of recording in seconds",
        default=60,
    )
    # parser.add_argument(
    #     "--devicethermal",
    #     type=int,
    #     help="Device ID of the thermal camera",
    #     default=2,
    # )
    # parser.add_argument(
    #     "--devicergb",
    #     type=int,
    #     help="Device ID of the rgb camera",
    #     default=1,
    # )
    parser.add_argument(
        "--dps",
        type=int,
        help="Vernier Data per second",
        default=20,
    )
    parser.add_argument(
        "--conn",
        type=str,
        help="Vernier connection type",
        default="usb",
    )

    parser.add_argument(
        "--runmin",
        action="store_true",
        default=False,
        help="Run the capture automatically in the next minute",
    )

    args = parser.parse_args()

    # get the camera id exactly
    graph = FilterGraph()
    thermal_cam_id = graph.get_input_devices().index("PureThermal (fw:v1.3.0)")
    rgb_cam_id = graph.get_input_devices().index("C270 HD WEBCAM")

    if not args.runmin:
        if args.cdown > 0:
            capture_start_time = dt.datetime.now() + dt.timedelta(seconds=args.cdown)
            capture_start_time = capture_start_time.strftime("%H:%M:%S")
        else:
            capture_start_time = args.rstime

    if args.runmin:
        nowtime = dt.datetime.now()
        nowtime = nowtime.strftime("%H:%M")
        print(nowtime)
        nowtime = dt.datetime.strptime(nowtime, "%H:%M")
        nowtime = nowtime + dt.timedelta(seconds=60)
        capture_start_time = nowtime.strftime("%H:%M:%S")

    runcapture(
        args.name,
        capture_start_time,
        args.duration,
        thermal_cam_id,
        rgb_cam_id,
        args.conn,
        args.dps,
    )
