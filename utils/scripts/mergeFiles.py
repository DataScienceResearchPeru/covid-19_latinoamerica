import pandas as pd
import numpy as np
import argparse
import os
import glob
import re

ap = argparse.ArgumentParser()
ap.add_argument('-p', "--path", required=True, help="Path to directory containing daily files")
ap.add_argument('-o', "--output", required=True, help="Output file name")
args = vars(ap.parse_args())

# Set file directory and set output filename
path = os.path.dirname(args['path'])
out = os.path.join("./", args["output"])


# Get all csv files in directory. Files must be in the format YYYY-mm-dd.csv
def glob_re(pattern, strings):
    return filter(re.compile(pattern).match, strings)


filenames = list(glob_re(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\.csv)', os.listdir(path)))

dates = [f.replace(".csv", "") for f in filenames]

df_master = pd.DataFrame()

for file in filenames:
    df_tmp = pd.read_csv(os.path.join(path, file))
    df_tmp["Date"] = file.replace(".csv", "")
    df_master = df_master.append(df_tmp)

df_master["Date"] = pd.to_datetime(df_master["Date"])

df_master.to_csv(f"{out}.csv")
