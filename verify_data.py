import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import os
import datetime as dt
import math
import argparse


def verify_start_end_dur(subjectname, the_type):
    """
    This function verifies the start, end and duration of the data
        Args
            subjectname: name of the subject
            type: type of data ('rgb', 'thermal', 'vernier')
        Returns
            1. The directory / file path of the data
            2. Number of files in the directory / Number of row in the file
            3. Start Time
            4. End Time
            5. Duration
            6. Sampling Rate
            7. Status (True/False)
    """
    ROOT = "dataset"

    if the_type is not "vernier":
        if the_type == "rgb":
            ext = "jpg"
        else:
            ext = "csv"

        the_dirpath = os.path.join(ROOT, subjectname, the_type)

        # List all files
        filelist = glob(os.path.join(the_dirpath, f"*.{ext}"))

        filelist = sorted(
            filelist, key=lambda x: int(os.path.basename(x).split(".")[0])
        )
        num_files = len(filelist)

        # get the first filename, only filename not the path. Then identify the start time
        first_file = os.path.basename(filelist[0])
        first_file = dt.datetime.strptime(
            first_file.split("_")[1]
            + first_file.split("_")[2]
            + first_file.split("_")[3][0:-4],
            "%Y%m%d%H%M%S%f",
        )

        # get the last filename, only filename not the path. Then identify the end time
        last_file = os.path.basename(filelist[-1])
        last_file = dt.datetime.strptime(
            last_file.split("_")[1]
            + last_file.split("_")[2]
            + last_file.split("_")[3][0:-4],
            "%Y%m%d%H%M%S%f",
        )

        # get the duration
        duration = last_file - first_file

        # validate fps
        fps = num_files / duration.total_seconds()

        # status is true if the fps for rgb is 30 and for thermal is 8
        if the_type == "rgb":
            status = int(fps) == 30
        else:
            status = int(fps) == 8

        return the_dirpath, num_files, first_file, last_file, duration, fps, status

    else:
        filename = f"{subjectname}_vernier.csv"
        csv_path = os.path.join(ROOT, subjectname, the_type, filename)

        # load csv using pandas
        df = pd.read_csv(csv_path, header=None)
        df.columns = ["TIME", "RR", "ECG"]
        length_of_data = len(df)

        # get the start time
        start_time = df["TIME"][0]
        start_time = dt.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")

        # get the end time
        end_time = df["TIME"][length_of_data - 1]
        end_time = dt.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

        # get the duration
        duration = end_time - start_time

        # validate fps
        fps = length_of_data / duration.total_seconds()

        # check if there's null
        null = df.isnull().values.any()

        # status is true if fps = 20 and there is no null
        status = int(fps) == 20 and not null

        return csv_path, length_of_data, start_time, end_time, duration, fps, status


def plot_gt(subject, duration):
    # load the csv
    ROOT = "dataset"
    filename = f"{subject}_vernier.csv"
    csv_path = os.path.join(ROOT, subject, "vernier", filename)
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["TIME", "RR", "ECG"]

    # create timeaxis
    duration = duration.total_seconds()
    timeaxis = np.linspace(0, duration, len(df))

    # create subplots and save
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    ax1.plot(timeaxis, df["RR"])
    ax1.set_title("RR")
    ax2.plot(timeaxis, df["ECG"])
    ax2.set_title("ECG")

    savename = f"{subject}_gt.png"
    saveloc = os.path.join(ROOT, subject, savename)
    plt.savefig(saveloc)
    plt.show()


def generate_report(subject):
    ROOT = "dataset"
    item = ["rgb", "thermal", "vernier"]

    for source in item:
        (
            the_dirpath,
            num_files,
            first_file,
            last_file,
            duration,
            fps,
            status,
        ) = verify_start_end_dur(subject, source)
        if source == "vernier":
            plot_gt(subject, duration)

        # dump the report as txt
        filename = f"{subject}_report.txt"
        saveloc = os.path.join(ROOT, subject, filename)

        # check if the file exists, if not, create an empty txt
        if not os.path.exists(saveloc):
            with open(saveloc, "w") as f:
                f.write("")

        # write the report
        with open(saveloc, "a") as f:
            # write the source
            f.write(f"Source: {source}\n")
            f.write(f"Directory: {the_dirpath}\n")
            f.write(f"Number of files: {num_files}\n")
            f.write(f"Start Time: {first_file}\n")
            f.write(f"End Time: {last_file}\n")
            f.write(f"Duration: {duration}\n")
            f.write(f"Sampling Rate: {fps}\n")
            f.write(f"Status: {status}\n")
            f.write("\n")

    print(f"Report for {subject} is generated")

    # open the txt and show it on terminal
    with open(saveloc, "r") as f:
        print(f.read())


if __name__ == "__main__":
    # dirpath, num_files, first, last, dur, fps, status = verify_start_end_dur("martin60d", "vernier")
    # print(f"Directory Path: {dirpath}")
    # print(f"Number of files: {num_files}")
    # print(f"Start time: {first}")
    # print(f"End time: {last}")
    # print(f"Duration: {dur}")
    # print(f"FPS: {fps}")
    # print(f"Status: {status}")
    # plot_gt("martin60d", dur)
    # generate_report("martin60d")

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=str, help="subject name")
    args = parser.parse_args()
    generate_report(args.subject)
