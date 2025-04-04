import pandas as pd
import os


mydataset = {'Start': [],
             'End': [],
             'Delta': [],
             'Course': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv', mode='w', index=True, header=True)




total = pd.read_csv("/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv")

print(total)

for filename in os.listdir("/Users/thibaultvanni/PycharmProjects/Study/hours_done"):
    if "Done" not in os.path.join("/Users/thibaultvanni/PycharmProjects/Study/hours_done", filename):
        if filename not in  ["TOTALSTUDY.csv", ".DS_Store"]:
            file = pd.read_csv(os.path.join("/Users/thibaultvanni/PycharmProjects/Study/hours_done", filename), encoding='utf-8')
            file["Course"] = filename
            total = pd.concat([file, total], ignore_index=True)

total['Start'] = pd.to_datetime(total['Start'], format="mixed", dayfirst=True)
total.sort_values(by=['Start'], ascending=True, inplace=True)
total.to_csv("/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv", mode='w', index=True, header=True)

print(total)