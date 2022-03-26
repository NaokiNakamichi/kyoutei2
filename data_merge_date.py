
import pandas as pd

import glob

years = [2021]
months = [i for i in range(1, 13)]
days = [i for i in range(1, 32)]

before_files = glob.glob("dataset/rawdata_beforeinfo/*")
race_info_files = glob.glob("dataset/rawdata_syussouhyou/*")
result_info_files = glob.glob("dataset/rawdata_result/*")

for year_i in years:
    for month_i in months:
        for day_i in days:
            tmp_df_list = []
            date = f"{year_i}-{month_i}-{day_i}"

            before_name = [s for s in before_files if (s.split("/")[2].split("_")[0].split("-")[0] == f"{year_i}"
                                                       and s.split("/")[2].split("_")[0].split("-")[1] == f"{month_i}"
                                                       and s.split("/")[2].split("_")[0].split("-")[2] == f"{day_i}")]

            race_info_name = [s for s in race_info_files if (s.split("/")[2].split("_")[0].split("-")[0] == f"{year_i}"
                                                             and s.split("/")[2].split("_")[0].split("-")[
                                                                 1] == f"{month_i}"
                                                             and s.split("/")[2].split("_")[0].split("-")[
                                                                 2] == f"{day_i}")]

            result_info_name = [s for s in result_info_files if
                                (s.split("/")[2].split("_")[0].split("-")[0] == f"{year_i}"
                                 and s.split("/")[2].split("_")[0].split("-")[1] == f"{month_i}"
                                 and s.split("/")[2].split("_")[0].split("-")[2] == f"{day_i}")]

            for i, name in enumerate(before_name):
                before_df = pd.read_csv(name, index_col=0)
                race_info_df = pd.read_csv(race_info_name[i], index_col=0)
                result_df = pd.read_csv(result_info_name[i], index_col=0)

                tmp = pd.merge(race_info_df, before_df, on=["race_no", "place_cd"])
                hoge = pd.merge(result_df, tmp, on=["race_no", "place_cd"])
                hoge.to_csv(f"dataset/merge_data/{date}.csv", encoding='utf_8_sig')