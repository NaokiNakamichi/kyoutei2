import data_get
import time

import race_before_data


years = [2022]
months = [i for i in range(3,4)]
days = [i for i in range(14,15)]

for year_i in years:
    for month_i in months:
        for day_i in days:
            time.sleep(5)
            try:

                date = f"{year_i}-{month_i}-{day_i}"
                data_get.download_file('results', date)
                df = data_get.get_results(date)
                df.to_csv(f"dataset/rawdata_result/{date}_result.csv", encoding='utf_8_sig')
                print(f"success {date}",flush=True)


            except Exception as e:

                print(e, flush=True)
