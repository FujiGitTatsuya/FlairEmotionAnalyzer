import math

pi = math.pi

def calc_emotionvalue(h, a, e, time, c0, 
                      eeg_sum, hr_sum,
                      start_f, end_f, count, data_start, period_d, data_end):
    start = start_f
    end = end_f
    d_start = data_start
    d_end = data_end

    if e == 100:
        print("event")
        if d_start == 0:
            d_start = 1
        else:
            #t_end = time.split('_')
            t_end = time
            #end = t_end[1]
            end = t_end
            count = period_d - 1
            d_end = 1
            d_start = 0

    if time == d_end - 1:
        t_end = time
        end = t_end
        count = period_d - 1

    hr = h
    awake = a

    eeg_sum = eeg_sum + awake
    hr_sum = hr_sum + hr
    c0 = c0 + 1

    count = count + 1

    if count == period_d:
        #t_end = time.split('_')
        t_end = time
        #end = t_end[1]
        end = t_end

    #data_start = d_start

    return eeg_sum, hr_sum, start, end, count, c0, d_start

def calc_emotionvalue_alpha(h, a, time, c0, 
                            eeg_sum, hr_sum,
                            start_f, end_f, count, data_start, period_d, data_end):
    start = start_f
    end = end_f
    d_start = data_start
    d_end = data_end

    if time == start:
        d_start = 1

    if time == d_end:
        t_end = time
        end = t_end
        count = period_d - 1
        d_start = 0

    hr = h
    awake = a

    eeg_sum = eeg_sum + awake
    hr_sum = hr_sum + hr
    c0 = c0 + 1

    count = count + 1

    if count == period_d:
        #t_end = time.split('_')
        t_end = time
        #end = t_end[1]
        end = t_end

    #data_start = d_start

    return eeg_sum, hr_sum, start, end, count, c0, d_start

def create_emotionlabels(eeg_sum, hr_sum, eeg_ave, hr_ave, c0):

    eeg = (eeg_sum/c0) - eeg_ave
    hr = (hr_sum/c0) - hr_ave
    #print(str(eeg) + ", " + str(hr))

    angle = math.atan2(eeg,hr) * 180/pi
    angle = int(angle)
    if(angle<0):
        angle = 360 + angle
    #angle = int(angle)

    if 0 <= angle <= 90:
        n = "Happy"
        fc = "rgba(255, 255, 0, 255)"
    elif 90 < angle <= 180:
        n = "Tense"
        fc = "rgba(255, 0, 0, 255)"
    elif 180 < angle <= 270:
        n = "Sad"
        fc = "rgba(0, 0, 255, 255)"
    elif 270 < angle <= 360:
        n = "Relax"
        fc = "rgba(0, 255, 0, 255)"

    eeg_sum = 0.0
    hr_sum = 0.0
    
    return n, fc, eeg_sum, hr_sum