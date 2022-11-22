import argparse
import subprocess
import os


def main(theargs):
    # os.system(f"start python junkfiles-a.py --sampleargs {theargs}")
    # os.system(f"start python junkfiles-b.py --sampleargs {theargs}")

    # subprocess.call(f"start python junkfiles-a.py --sampleargs {theargs}", shell=True)
    # subprocess.call(f"start python junkfiles-b.py --sampleargs {theargs}", shell=True)

    subprocess.Popen(
        f"start python junkfiles-a.py --sampleargs {theargs}",
        shell=True,
    )
    subprocess.Popen(
        f"start python junkfiles-b.py --sampleargs {theargs}",
        shell=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampleargs", type=str, help="Sample args")
    args = parser.parse_args()

    main(args.sampleargs)
