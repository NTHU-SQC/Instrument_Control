import numpy as np

"""
Create the following functions to build waveform 
"""
def gauss(sigma, x, shift=0)->float:
    return np.exp((-1 * (x - shift)**2) / (2 * sigma**2))

def exp_rising(delta_t, tau_pos)->float:
    return np.exp(delta_t / tau_pos)   


"""
Domain-transform
"""
def domain_trans(want, time, pos, samp_rat=10**9,typ="time-pos"):
    """
    A Convertor for domain-transform between time domain and points position domain
    Demonstrate:
        1/1e9[1/GigaSamp]                          t0_pos(want)    
    ---------------------------- [sec/pnt] =  ----------------------------[sec/pnt]
        1                                          pos_pts
                                 
    Args:
        want: the start point (sec)
        time: duration within one_sequence
        samp_rate: sampling rate 
        typ:
            "time-pos": select points position scale
    Return:
        if typ is "time-pos", then return the points position
        else return the time scale
    """
    if typ == "time-pos":
        for i in range(len(time)):
            """
            a = time[i] + 1/samp_rat 
            b = time[i] - 1/samp_rat
            inequality: a>=t0>=b
            """
            if time[i] + 1/samp_rat >= want and time[i] - 1/samp_rat <= want:
                return int(pos[i])
    else:
        for i in range(len(pos)):
            if time[i] + 1/samp_rat >= want and time[i] -1/samp_rat <= want:
                return time[i]