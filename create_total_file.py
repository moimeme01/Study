import pandas as pd
import os
from main import initial_path, actual_period

mydataset = {'Start': [],
             'End': [],
             'Delta': [],
             'Course': []}
myvar = pd.DataFrame(mydataset)
path = initial_path + '/TOTALSTUDY.csv'
myvar.to_csv(path, mode='w', index=True, header=True)


total = pd.read_csv(path)

print(total)

for filename in os.listdir(initial_path + "/hours_done_" + actual_period):
    if "Done" not in os.path.join(initial_path, "/hours_done_", actual_period, filename):
        if filename not in  ["TOTALSTUDY.csv", ".DS_Store"]:
            file = pd.read_csv(os.path.join(initial_path, "/hours_done_", actual_period, filename), encoding='utf-8')
            file["Course"] = filename
            total = pd.concat([file, total], ignore_index=True)

total['Start'] = pd.to_datetime(total['Start'], format="mixed", dayfirst=True)
total.sort_values(by=['Start'], ascending=True, inplace=True)
total.to_csv(path, mode='w', index=True, header=True)

#print(total)