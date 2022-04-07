
import pandas as pd

df = pd.read_csv("dataset/all_data_2021.csv", index_col=0)

all_place_name = df['place_y'].unique()


for i_place_name in all_place_name:
    print(i_place_name)
    place_df_i = df.query(f'place_y == "{i_place_name}"')
    place_df_i.reset_index(drop=True,inplace=True)
    place_df_i.to_csv(f"dataset/place/{i_place_name}.csv", encoding='utf_8_sig')

