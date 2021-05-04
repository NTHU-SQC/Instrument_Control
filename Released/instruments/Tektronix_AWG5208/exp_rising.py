import numpy as np
import pylab as plt

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

def zero(total_points):
    return np.zeros(total_points)

if __name__ == '__main__':
    sampling_rate = 10**9                                               # awg sampling rate
    tau = 600*10**-9                                                    # characteristic time
    t0 = 2600*10**-9                                                    # start value(second)
    one_sequence = 10*10**-6                                            # duration within 10 microsec

    total_pts = int(one_sequence*sampling_rate)
    waveform_pos = np.linspace(0,total_pts,total_pts+1)                 # construct the point scale from 0 to 10000
    time = np.linspace(0,one_sequence,total_pts+1)                      # construct the time scale in one_sequence(unit:1e-9)


    #domain transform 
    tau_pos = int(tau*sampling_rate)
    t0_pos = domain_trans(t0, time, waveform_pos,                       # scale convert from time scale(1ns)
                          sampling_rate, typ="time-pos")                # to point scale


    delta_t = waveform_pos[:t0_pos]-np.linspace(t0_pos,t0_pos,t0_pos)
    pulse = np.exp(delta_t/tau_pos)
    # plt.plot([i for i in range(len(pulse))],pulse)  
    # plt.show()      
    waveform = zero(total_pts)
    waveform[:t0_pos] = pulse

    x = [i for i in range(len(waveform))]
    y = waveform
    plt.plot(x, y)
    plt.show()