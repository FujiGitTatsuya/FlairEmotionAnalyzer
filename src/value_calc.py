import statistics
import pandas as pd

def calc_rest_avarage(df, ticker1, ticker2, ticker3):
    c0 = 0
    rest_hr = 0
    rest_eeg = 0
    if(ticker1==ticker2):
        for j, row in df.iterrows():
            if(row['stimu_num']==0):
                rest_hr = rest_hr + row[ticker3]
                rest_eeg = rest_eeg + row[ticker1]
                c0 = c0 + 1
    else:
        for j, row in df.iterrows():
            if(row['stimu_num']==0):
                rest_hr = rest_hr + row[ticker3]
                rest_eeg = rest_eeg + (row[ticker1]/row[ticker2])
                c0 = c0 + 1
    rest_hr=rest_hr/c0
    rest_eeg=rest_eeg/c0

    return rest_hr, rest_eeg

def calc_rest_average_clean(df, eeg_data, ticker3):
    c0 = 0
    rest_hr = 0
    rest_eeg = 0
    for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
        if num == 0:
            rest_hr = rest_hr + hr
            rest_eeg = rest_eeg + eeg
            c0 = c0 + 1
    rest_hr=rest_hr/c0
    rest_eeg=rest_eeg/c0

    return rest_hr, rest_eeg

def calc_rest_average_list(df, eeg_data, ticker3, rest_n):
    c0 = 0
    rest_hr = 0
    rest_eeg = 0
    rest_hr_list = []
    rest_eeg_list = []
    for r_n in rest_n:
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == r_n:
                rest_hr = rest_hr + hr
                rest_eeg = rest_eeg + eeg
                c0 = c0 + 1
        rest_hr=rest_hr/c0
        rest_eeg=rest_eeg/c0
        rest_hr_list.append(rest_hr)
        rest_eeg_list.append(rest_eeg)
        c0 = 0
        rest_hr = 0
        rest_eeg = 0

    return rest_hr_list, rest_eeg_list

def calc_stml_average(df, case_size, ticker1, ticker2, ticker3, rest_hr, rest_eeg,
                      stimu_n, x_data, y_data, stml_hr_avr, stml_eeg_avr, stml1_hr, stml1_eeg):
    c1 = 0
    #Calculate the average of HR and EEG during each stimulus
    for i in range(case_size):
        if(ticker1==ticker2):
            for j, row in df.iterrows():
                if(row['stimu_num']==stimu_n[i]):
                    stml1_hr = stml1_hr + row[ticker3]
                    stml1_eeg = stml1_eeg + row[ticker1]
                    c1 = c1 + 1
        else:
            for j, row in df.iterrows():
                if(row['stimu_num']==stimu_n[i]):
                    stml1_hr = stml1_hr + row[ticker3]
                    stml1_eeg = stml1_eeg + (row[ticker1]/row[ticker2])
                    c1 = c1 + 1
        stml1_hr=stml1_hr/c1
        stml1_eeg=stml1_eeg/c1
        x_data.append((stml1_hr-rest_hr))
        y_data.append((stml1_eeg-rest_eeg))
        stml_hr_avr.append(stml1_hr)
        stml_eeg_avr.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        c1=0

    return x_data, y_data, stml_hr_avr, stml_eeg_avr

def calc_stml_average_clean(df, eeg_data, case_size, ticker3, rest_hr, rest_eeg,
                            stimu_n, x_data, y_data, stml_hr_avr, stml_eeg_avr, stml1_hr, stml1_eeg):
    c1 = 0
    #Calculate the average of HR and EEG during each stimulus
    for i in range(case_size):
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == stimu_n[i]:
                stml1_hr = stml1_hr + hr
                stml1_eeg = stml1_eeg + eeg
                c1 = c1 + 1
        stml1_hr=stml1_hr/c1
        stml1_eeg=stml1_eeg/c1
        x_data.append((stml1_hr-rest_hr))
        y_data.append((stml1_eeg-rest_eeg))
        stml_hr_avr.append(stml1_hr)
        stml_eeg_avr.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        c1=0

    return x_data, y_data, stml_hr_avr, stml_eeg_avr

def calc_stml_average_list(df, eeg_data, case_size, ticker3, rest_hr_list, rest_eeg_list,
                           stimu_n, x_data, y_data, stml_hr_avr, stml_eeg_avr, stml1_hr, stml1_eeg):
    c1 = 0
    #Calculate the average of HR and EEG during each stimulus
    for stimu_num in stimu_n:
        eeg_ave = rest_eeg_list[stimu_n.index(stimu_num)]
        hr_ave = rest_hr_list[stimu_n.index(stimu_num)]
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == stimu_num:
                stml1_hr = stml1_hr + hr
                stml1_eeg = stml1_eeg + eeg
                c1 = c1 + 1
        stml1_hr=stml1_hr/c1
        stml1_eeg=stml1_eeg/c1
        x_data.append((stml1_hr-hr_ave))
        y_data.append((stml1_eeg-eeg_ave))
        stml_hr_avr.append(stml1_hr)
        stml_eeg_avr.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        c1=0

    return x_data, y_data, stml_hr_avr, stml_eeg_avr

def calc_rest_median(df, ticker1, ticker2, ticker3, rs_hr, rs_eeg):
    rest_hr = 0
    rest_eeg = 0
    #Calculate median HR and EEG at rest
    if(ticker1==ticker2):
        for j, row in df.iterrows():
            if(row['stimu_num']==0):
                rs_hr.append(row[ticker3])
                rs_eeg.append(row[ticker1])
    else:
        for j, row in df.iterrows():
            if(row['stimu_num']==0):
                rs_hr.append(row[ticker3])
                rs_eeg.append((row[ticker1]/row[ticker2]))
    rest_hr=statistics.median(rs_hr)
    rest_eeg=statistics.median(rs_eeg)

    return rest_hr, rest_eeg

def calc_rest_median_clean(df, eeg_data, ticker3, rs_hr, rs_eeg):
    rest_hr = 0
    rest_eeg = 0
    #Calculate median HR and EEG at rest
    for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
        if num == 0:
            rs_hr.append(hr)
            rs_eeg.append(eeg)
    rest_hr=statistics.median(rs_hr)
    rest_eeg=statistics.median(rs_eeg)

    return rest_hr, rest_eeg

def calc_rest_median_list(df, eeg_data, ticker3, rs_hr, rs_eeg, rest_n):
    rest_hr = []
    rest_eeg = []
    #Calculate median HR and EEG at rest
    for r_n in rest_n:
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == r_n:
                rs_hr.append(hr)
                rs_eeg.append(eeg)
        rest_hr.append(statistics.median(rs_hr))
        rest_eeg.append(statistics.median(rs_eeg))
        rs_hr = []
        rs_eeg = []

    return rest_hr, rest_eeg

def calc_stml_median(df, case_size, ticker1, ticker2, ticker3, rest_hr, rest_eeg,
                     stimu_n, x_data, y_data, stml_hr_med, stml_eeg_med):
    sl_hr = []
    sl_eeg = []
    #Calculate median HR and EEG at each stimulation
    for i in range(case_size):
        if(ticker1==ticker2):
            for j, row in df.iterrows():
                if(row['stimu_num']==stimu_n[i]):
                    sl_hr.append(row[ticker3])
                    sl_eeg.append(row[ticker1])
        else:
            for j, row in df.iterrows():
                if(row['stimu_num']==stimu_n[i]):
                    sl_hr.append(row[ticker3])
                    sl_eeg.append(row[ticker1]/row[ticker2])
        stml1_hr=statistics.median(sl_hr)
        stml1_eeg=statistics.median(sl_eeg)
        x_data.append((stml1_hr-rest_hr))
        y_data.append((stml1_eeg-rest_eeg))
        stml_hr_med.append(stml1_hr)
        stml_eeg_med.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        sl_hr=[]
        sl_eeg=[]

    return x_data, y_data, stml_hr_med, stml_eeg_med

def calc_stml_median_clean(df, eeg_data, case_size, ticker3, rest_hr, rest_eeg,
                            stimu_n, x_data, y_data, stml_hr_med, stml_eeg_med):
    sl_hr = []
    sl_eeg = []
    #Calculate median HR and EEG at each stimulation
    for i in range(case_size):
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == stimu_n[i]:
                sl_hr.append(hr)
                sl_eeg.append(eeg)
        stml1_hr=statistics.median(sl_hr)
        stml1_eeg=statistics.median(sl_eeg)
        x_data.append((stml1_hr-rest_hr))
        y_data.append((stml1_eeg-rest_eeg))
        stml_hr_med.append(stml1_hr)
        stml_eeg_med.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        sl_hr=[]
        sl_eeg=[]

    return x_data, y_data, stml_hr_med, stml_eeg_med

def calc_stml_median_list(df, eeg_data, case_size, ticker3, rest_hr_list, rest_eeg_list,
                            stimu_n, x_data, y_data, stml_hr_med, stml_eeg_med):
    sl_hr = []
    sl_eeg = []
    #Calculate median HR and EEG at each stimulation
    for stimu_num in stimu_n:
        eeg_med = rest_eeg_list[stimu_n.index(stimu_num)]
        hr_med = rest_hr_list[stimu_n.index(stimu_num)]
        for num, eeg, hr in zip(df['stimu_num'], eeg_data, df[ticker3]):
            if num == stimu_num:
                sl_hr.append(hr)
                sl_eeg.append(eeg)
        stml1_hr=statistics.median(sl_hr)
        stml1_eeg=statistics.median(sl_eeg)
        x_data.append((stml1_hr-hr_med))
        y_data.append((stml1_eeg-eeg_med))
        stml_hr_med.append(stml1_hr)
        stml_eeg_med.append(stml1_eeg)
        stml1_hr=0
        stml1_eeg=0
        sl_hr=[]
        sl_eeg=[]

    return x_data, y_data, stml_hr_med, stml_eeg_med