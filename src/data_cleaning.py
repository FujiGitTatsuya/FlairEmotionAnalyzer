def data_cleaning(df):
    drop_index = []
    index_count = 0

    for th, de, la, ha, lb, hb, lg, mg in zip(df['theta'], df['delta'], df['low_alpha'], df['high_alpha'], 
                                            df['low_beta'], df['high_beta'], df['low_gamma'], df['mid_gamma']):
        
        if 0 in [th, de, la, ha, lb, hb, lg, mg]:
            drop_index.append(index_count)

        index_count = index_count + 1

    df_clean = df.drop(index = drop_index)

    return df_clean