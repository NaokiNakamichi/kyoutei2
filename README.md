## 競艇 データ分析

## 目的

回収率100％越え

## 競艇について

成長中の公営ギャンブルである。
CMや美人選手、ネット投票などが影響か。

### 競艇用語
- 枠なり
進入が枠順通り
  
### カラム説明
- area 所属支部
- class 選手階級
- glob-win 全国勝率
- glob_in2 全国2連帯率
- loc_win 当地勝率
- loc_in2 当地2連帯率
- ET1 展示タイム
- tilt_1 チルト角度
- EST_1　展示スタートタイム
- ESC_1 展示スタートコース
- wether 天気
- air_t 気温 
- wind_d 風向 (16方向 + 無風)
- wind_v 風速
- water_t 水温
- wave_h 波高

## 競艇とデータ分析について

参考リンク　素素人が競艇AIを作ってみる 
https://qiita.com/Norimax/items/7540ebcb6b07711260e6

- 使う (numerical)	
  - 日程(n日目), 年齢, 体重,
  - 勝率 & 2連帯率
  - (全国/当地/モーター/ボート)	展示タイム, 
  - 展示スタートタイミング, 
  - 展示スタートコース,
  - チルト角度, 風速, 
  - 水温, 波高
- 使う(categorical)
  - 会場, レース種別	天気, 風向
- 使わない	
  - タイトル, コース距離, 締切時刻, 登番, 選手名, 所属支部, モーター番号, ボート番号	