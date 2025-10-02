import pandas as pd
import os
from settings import *


def create_total_file_function():
    mydataset = {'Start': [],
                 'End': [],
                 'Delta': [],
                 'Course': []}
    myvar = pd.DataFrame(mydataset)
    path = hours_done_path + '/TOTALSTUDY.csv'
    myvar.to_csv(path, mode='w', index=True, header=True)


    total = pd.read_csv(path)


    for filename in os.listdir(initial_path + "/hours_done_" + actual_period):
        if "Done" not in os.path.join(initial_path, "/hours_done_", actual_period, filename):
            if filename not in  ["TOTALSTUDY.csv", ".DS_Store"]:
                file = pd.read_csv(os.path.join(initial_path + "/hours_done_" + actual_period, filename), encoding='utf-8')
                file["Course"] = filename
                total = pd.concat([file, total], ignore_index=True)

    total['Start'] = pd.to_datetime(total['Start'], format="mixed", dayfirst=True)
    total.sort_values(by=['Start'], ascending=True, inplace=True)
    total.to_csv(path, mode='w', index=True, header=True)
    return

create_total_file_function()
#print(total)