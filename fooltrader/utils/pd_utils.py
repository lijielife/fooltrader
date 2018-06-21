# -*- coding: utf-8 -*-
import pandas as pd


def kdata_df_save(df, to_path, calculate_change=False):
    df = df.drop_duplicates(subset='timestamp', keep='last')
    df = df.set_index(df['timestamp'], drop=False)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    if calculate_change:
        pre_close = None
        for index in df.index:
            if pd.notna(df.loc[index, ['preClose', 'change', 'changePct']]).all():
                continue
            current_close = df.loc[index, 'close']
            if pre_close:
                df.loc[index, 'preClose'] = pre_close
                change = current_close - pre_close
                df.loc[index, 'change'] = change
                df.loc[index, 'changePct'] = change / current_close
            pre_close = df.loc[index, 'close']
    df.to_csv(to_path, index=False)
