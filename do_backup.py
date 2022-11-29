import os
from pathlib import Path
import zipfile
import argparse

def zipthefolder(pathtozip, savelocation):
    print(f"Savelocation: {savelocation}")
    print(f"Pathtozip: {pathtozip}")
    # Zip up the folder. Start zip from one level down from the root folder
    zipf = zipfile.ZipFile(savelocation, 'w', zipfile.ZIP_DEFLATED)
    print(f"Starting to zip {pathtozip}")
    for root, dirs, files in os.walk(pathtozip):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    print(f"Zipped: {pathtozip} to {savelocation}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup a folder')
    parser.add_argument('--subject', help='Folder to backup')
    parser.add_argument('--saveloc', help='Location to save the backup')
    args = parser.parse_args()

    datasetroot = "./dataset"
    pathtozip = os.path.join(datasetroot, args.subject)
    savelocation = f"{args.saveloc}/{args.subject}.zip"

    zipthefolder(pathtozip, savelocation)