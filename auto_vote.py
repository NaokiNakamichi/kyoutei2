import pandas as pd
import numpy as np
import data_get
import race_before_data
import pickle
import time
import datetime
import before_odds
import sched

import collections

all_record = []


def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def hensachi(x):
    x = x.astype(float)
    if x.std() == 0:
        return pd.Series(np.full(6, 50.0))

    hensa = (x - x.mean()) * 10 / x.std() + 50

    return hensa


def rank_mapper(x):
    if 'A1' in x:
        y = 4
    elif 'A2' in x:
        y = 3
    elif 'B1' in x:
        y = 2
    else:
        y = 1
    return y


def create_ex_time(x):
    date_format = '%Y-%m-%d %H:%M:%S'
    diff = datetime.timedelta(seconds=5)

    date_dt = datetime.datetime.strptime(x, date_format)
    date_dt_new = date_dt - diff

    date_str_new = date_dt_new.strftime(date_format)
    return date_str_new


def ex(index, row):
    record = []
    time.sleep(1)
    place = row["place"]
    print(f"開催場所：{place}")
    place_cd, race_no, date = row["place_cd"], row["race_no"], row["date"]
    deadline = row["deadline"]
    print(f"レース番号：{race_no}")
    record.append(place_cd)
    record.append(race_no)
    bi = race_before_data.get_beforeinfo(date, place_cd, race_no)
    tmp = pd.merge(pd.DataFrame(row).T, pd.DataFrame(bi).T, on=["race_no", "place_cd"])
    usecols = [f'{k}_{i}' for k in ('class', 'glob_win', 'glob_in2',
                                    'loc_win', 'loc_in2', 'moter_in2', 'boat_in2', 'EST', 'ESC')
               for i in range(1, 7)]
    usecols += [f'ET_{i}'
                for i in range(1, 7)]

    tmp = tmp[usecols]

    for i in range(1, 7):
        col_name_class = f"class_{i}"
        tmp[col_name_class] = tmp[col_name_class].map(rank_mapper)
    class_col = [s for s in tmp.columns if "class" in s]

    tmp.loc[:, class_col] = tmp.loc[:, class_col].apply(hensachi, axis=1)

    hensa_col = ['glob_win', 'glob_in2', 'loc_win', 'loc_in2', 'moter_in2', 'boat_in2', 'EST', "ET", "ESC"]

    for i in hensa_col:
        class_col = [s for s in tmp.columns if i in s]
        tmp[class_col] = tmp.loc[:, class_col].apply(hensachi, axis=1)

    X = tmp.values
    y_pred = model.predict(X)
    # テストデータのクラス予測確率 (各クラスの予測確率 [クラス0の予測確率,クラス1の予測確率,クラス2の予測確率...] を返す)
    y_pred_prob = model.predict_proba(X)
    hoge = before_odds.get_odds(BET_TYPE="tf", race_no=race_no, place_cd=place_cd, date=date)

    before_odds_list = []

    for i in hoge.select("td.oddsPoint"):
        before_odds_list.append(i.text)

    hoge = [float(s) for s in before_odds_list]
    # print(f"予測確率：{y_pred_prob}")
    # print(f"直前オッズ:{hoge}")
    # print(f"オッズ＊予測{hoge*y_pred_prob}")
    oddsinpred = np.argmax(hoge * y_pred_prob)
    record.append(hoge)
    record.append(oddsinpred + 1)
    record.append(hoge[oddsinpred])
    umami = np.max(hoge * y_pred_prob)
    print(f"旨味係数：{umami}")
    if umami > 2.0:
        print("購入!!!!!!!!")
        record.append(1)
    else:
        record.append(0)

    print(f"開催場所：{place}, レース番号：{race_no},オッズ込み予想{oddsinpred + 1},オッズ{hoge[oddsinpred]}")

    flat = list(flatten(record))
    all_record.append(flat)


date = '2022-04-04'
data_get.download_file('racelists', date)
df_race = data_get.get_racelists(date)

df_race.to_csv(f"dataset/rawdata_syussouhyou/{date}_race_list.csv", encoding='utf_8_sig')
df_race = df_race.sort_values(by="deadline").reset_index(drop=True)
deadlines_list = df_race["deadline"].values

filename = '0402model.sav'
model = pickle.load(open(filename, 'rb'))

format_deadlines = [date + " " + s + ":00" for s in deadlines_list]
ex_time_list = list(map(create_ex_time, format_deadlines))

for index, row in df_race.iterrows():

    ex_time = ex_time_list[index]

    try:
        s = sched.scheduler(time.time)
        t = time.strptime(ex_time, '%Y-%m-%d %H:%M:%S')
        t = time.mktime(t)
        s.enterabs(t, 1, ex, kwargs={'index': index, 'row': row})
        s.run()
        # jissai.append(sum(tmp,[]))
        print("============================")

    except Exception as e:
        print("hoge")
        print(e, flush=True)

columns = ['place_cd', 'race_no', 'odds1', 'odds2', 'odds3', 'odds4', 'odds5', 'odds6', 'hunaken', 'before_odds',
           'is_buy']
hoge = pd.DataFrame(all_record)
hoge.columns = columns
hoge.to_csv(f"auto_{date}.csv", columns=columns)
