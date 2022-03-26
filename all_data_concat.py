
import pandas as pd
import glob

files = glob.glob("dataset/merge_data/*")
print(len(files))

datalist = []
for file_i in files:
    datalist.append(pd.read_csv(f"{file_i}",index_col=0))

df = pd.concat(datalist, axis=0)

drop_list = [s for s in df.columns if "_x" in s]
drop_df = df.drop(drop_list, axis=1)
drop_df.to_csv("dataset/all_data_2021.csv", encoding='utf_8_sig')

