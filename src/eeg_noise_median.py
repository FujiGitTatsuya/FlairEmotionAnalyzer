import numpy as np
import pandas as pd
import statistics
import scipy.interpolate as scipl

def noise_median(df, ticker1, ticker2):
    #input data
    eeg_data = []
    index = []
    i = 0
    if ticker1 == ticker2:
        for data in df[ticker1]:
            eeg_data.append(data)
            index.append(i)
            i = i + 1
    else:
        for data in (df[ticker1]/df[ticker2]):
            eeg_data.append(data)
            index.append(i)
            i = i + 1

    #delete noise
    eeg_mean = statistics.mean(eeg_data)
    eeg_std = statistics.stdev(eeg_data)
    eeg_med = statistics.median(eeg_data)
    eeg_data = np.array(eeg_data)
    mad = statistics.median(np.abs(eeg_data - eeg_med))

    eeg_new = []
    index_new = []
    for i, a in enumerate(eeg_data):
        if np.abs(a - eeg_med)/mad > 1.4826:
            continue
        eeg_new.append(a)
        index_new.append(index[i])
    
    #補完
    f_sci = scipl.Akima1DInterpolator(index_new, eeg_new)

    #平滑化
    window = 5
    w = np.ones(window)/window
    eeg_clean = np.convolve(f_sci(index), w, mode='same')

    eeg_clean = pd.DataFrame(eeg_clean, columns=['eeg'])

    return eeg_clean

def noise_disc(df, ticker1, ticker2):

    index_x = []
    eeg_data = []
    i = 0
    if ticker1 == ticker2:
        for data in df[ticker1]:
            eeg_data.append(data)
            index_x.append(i)
            i = i + 1
    else:
        for data in df[ticker1]/df[ticker2]:
            eeg_data.append(data)
            index_x.append(i)
            i = i + 1

    eeg_med = statistics.median(eeg_data)
    eeg_data = np.array(eeg_data)
    mad = statistics.median(np.abs(eeg_data - eeg_med))

    x_disc = []
    y_disc = []
    for point, eeg in zip(index_x, eeg_data):
        if np.abs(eeg - eeg_med)/mad > 1.4826:
            x_disc.append(point)
            y_disc.append(eeg)

    return x_disc, y_disc
