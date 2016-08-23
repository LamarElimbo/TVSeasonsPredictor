import settings
import os
import csv
import pandas as pd
import glob

def createMasterDatabase():

    os.chdir('..')
    os.chdir(settings.DATA_DIR)

    all_files = glob.glob(os.path.join("*.csv"))
    print('files: ', all_files, 'files len: ', len(all_files))
    df = pd.concat(pd.read_csv(f) for f in all_files[:])
    return df


if __name__ == "__main__":
    master = createMasterDatabase()
    print('master = ', master)
    master.to_csv(settings.MASTER_FILE)
