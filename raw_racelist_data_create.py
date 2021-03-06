import data_get
import time

import race_before_data


years = [2022]
months = [i for i in range(1,4)]
days = [i for i in range(1,32)]

for year_i in years:
    for month_i in months:
        for day_i in days:
            time.sleep(5)
            try:

                date = f"{year_i}-{month_i}-{day_i}"
                data_get.download_file('racelists', date)
                df = data_get.get_racelists(date)
                df.to_csv(f"dataset/rawdata_syussouhyou/{date}_race_list.csv", encoding='utf_8_sig')
                print(f"success {date}",flush=True)

            except:
                print("error",flush=True)
