import data_get
import time
import pandas as pd
import datetime

import race_before_data


years = [2022]
months = [i for i in range(1,4)]
days = [i for i in range(1,32)]
race_no = [i for i in range(1,13)]
place_cd = [i for i in range(1,25)]

for year_i in years:
    for month_i in months:
        for day_i in days:
            tmp_df_list = []
            date = f"{year_i}-{month_i}-{day_i}"
            for place_cd_i in place_cd:
                for race_no_i in race_no:
                    time.sleep(1)
                    dt_now = datetime.datetime.now()

                    print(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
                    try:
                        df = race_before_data.get_beforeinfo(date, place_cd_i, race_no_i)
                        tmp_df_list.append(df)
                        print(f"success {date} place {place_cd_i} race-no {race_no_i} ",flush=True)
                    except Exception as e:
                        print(f"false {date} place {place_cd_i} race-no {race_no_i} ",flush=True)
                        print(e, flush=True)
                        break



            try:
                df_date = pd.concat(tmp_df_list, axis=1)
                df_date.T.to_csv(f"dataset/rawdata_beforeinfo/{date}_before_info.csv", encoding='utf_8_sig')
                print(f"success {date} concat and to_csv", flush=True)
            except Exception as e:
                print(e, flush=True)
