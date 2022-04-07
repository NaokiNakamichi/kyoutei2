

from bs4 import BeautifulSoup
from requests import get

# 時間を制御する time モジュールから sleep をインポート
from time import sleep

# URLの固定部分を指定



#%%

def get_odds(BET_TYPE,race_no,place_cd, date):
    date = date.replace("-", "")
    place_cd = str(place_cd)
    if len(place_cd) == 1:
        place_cd = "0" + place_cd
    sleep(1)
    FIXED_URL = "https://www.boatrace.jp/owpc/pc/race/odds"
    # 舟券種別を指定
    # リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
    target_url = FIXED_URL + BET_TYPE + "?rno=" + str(race_no) \
                 + "&jcd=" + str(place_cd) + "&hd=" + date
    # BeautifulSoupにWebサイトのコンテンツを渡す
    html = get(target_url)
    soup = BeautifulSoup(html.content, 'html.parser')
    target_table_selector = "body > main > div > div > div > div.contentsFrame1_inner > div.grid.is-type2.h-clear > div:nth-child(1) > div.table1 > table"
    odds_table = soup.select_one(target_table_selector)

    return odds_table



