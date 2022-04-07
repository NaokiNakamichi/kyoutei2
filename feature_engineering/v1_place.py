import numpy as np
import pandas as pd
import glob

files = glob.glob("../dataset/place/*")
print(len(files))


for i_file in files:
    usecols = [f'{k}_{i}' for k in ('class', 'glob_win', 'glob_in2',
                                    'loc_win', 'loc_in2', 'moter_in2', 'boat_in2', 'EST', 'ESC')
               for i in range(1, 7)]
    usecols += [f'ET_{i}_y'
                for i in range(1, 7)]
    hoge = pd.read_csv(i_file)
    file_name = hoge["place_y"][0]

    tmp = hoge[usecols]


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


    for i in range(1, 7):
        col_name_class = f"class_{i}"
        tmp.loc[:, col_name_class] = tmp.loc[:, col_name_class].map(rank_mapper)
    class_col = [s for s in tmp.columns if "class" in s]


    def hensachi(x):
        if x.std() == 0:
            return np.full(6, 50.0)

        hensa = (x - x.mean()) * 10 / x.std() + 50

        return hensa


    tmp.loc[:, class_col] = tmp.loc[:, class_col].apply(hensachi, axis=1)

    hensa_col = ['glob_win', 'glob_in2', 'loc_win', 'loc_in2', 'moter_in2', 'boat_in2', 'EST', "ET", "ESC"]

    for i in hensa_col:
        class_col = [s for s in tmp.columns if i in s]
        tmp.loc[:, class_col] = tmp.loc[:, class_col].apply(hensachi, axis=1)

    tmp.to_csv(f"../dataset/v1_features/place/{file_name}_v1.csv")
