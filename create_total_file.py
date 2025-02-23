import pandas as pd
import os


mydataset = {'Start': [],
             'End': [],
             'Delta': [],
             'Course': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv', mode='w', index=True, header=True)

total = pd.read_csv("/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv")


for filename in os.listdir("/Users/thibaultvanni/PycharmProjects/Study/hours_done"):
    if "Done" not in os.path.join("/Users/thibaultvanni/PycharmProjects/Study/hours_done", filename):
        if filename != "TOTALSTUDY.csv":
            file = pd.read_csv(os.path.join("/Users/thibaultvanni/PycharmProjects/Study/hours_done", filename), encoding='utf-8')

            file["Course"] = filename
            total = pd.concat([file, total], ignore_index=True)

total.sort_values(by=['Start'], ascending=True, inplace=True)
total.to_csv("/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv", mode='w', index=True, header=True)

