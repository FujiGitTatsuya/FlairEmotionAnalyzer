import pandas as pd

def event_identify(df):
    event = []
    num_temp = 1000
    num_current = 0
    for s_num in df['stimu_num']:
        num_current = s_num
        if num_temp == 1000:
            num_temp = s_num
        
        if num_current != num_temp:
            event.append(100)
        else:
            event.append(0)
        
        num_temp = num_current

    return event