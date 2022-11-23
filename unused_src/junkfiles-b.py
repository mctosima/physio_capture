import datetime as dt
from time import sleep
import argparse
import os
import numpy as np


def main(theargs):
    # os.system("conda activate py37vernier")
    print(f"Junkfiles-b.py: {dt.datetime.now()} | {theargs}")
    sleep(3)
    print(f"Ending of Junkfiles-b.py: {dt.datetime.now()}")
    thearray = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Array: {thearray}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampleargs", type=str, help="Sample args")
    args = parser.parse_args()

    main(args.sampleargs)
