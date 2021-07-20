#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : WaveForm_Editor.py
# Author            : Liam Lin
# Date              : 13.07.2021
# Last Modified Date: 19.07.2021
# Last Modified By  : Liam Lin
import numpy as np



def TimeSpan(span=.0, sampling_rate=1, delEnd=True):
    
    points = int(span * sampling_rate + 1)
    x = np.linspace(0, span, points)
    end = None
    if delEnd:
        end = -1
    return x[:end]

###Create Building blocks of the waveform 
 
def GaussianPulse(sigmaLen, flatLen, Nsigma = 4):
    
    pulsewidth = flatLen + Nsigma*sigmaLen*2 + 1;
    GaussWfm = np.empty(pulsewidth, dtype=np.float64)
    Pulselist = np.linspace(0, pulsewidth-1, pulsewidth, dtype=int)
    GaussPeak = Nsigma * sigmaLen
    for i in range(len(Pulselist)):
    #(section 1)
        if(i <= GaussPeak):
            GaussWfm[i] = 1*(np.exp((-1*(Pulselist[i]-GaussPeak)**2/(2*sigmaLen**2))))
    #(section 2)
        elif(i > GaussPeak and i < GaussPeak + flatLen):
            GaussWfm[i] = 1
    #(section 3)
        else:
            GaussWfm[i] = 1*(np.exp((-1*(Pulselist[i]-flatLen-GaussPeak)**2/(2*sigmaLen**2))))
    
    variables = {"function":GaussianPulse,"Pulsewidth":pulsewidth,"FlatLength":flatLen,"SigmaLength":sigmaLen}

    return packer(Pulselist, GaussWfm, variables, appendRule=[True,True], name="")


def SquarePulse(flatLen):
    
    SquareWfm = np.ones(flatLen)
    Pulselist = np.linspace(0,flatLen-1,flatLen,dtype=int)
    variables = {"function":SquarePulse,"Pulsewidth":flatLen}

    return packer(Pulselist, SquareWfm, variables, [True, True], name="")


def NullPulse(nullLen):

    NullWfm = np.zeros(nullLen,dtype = np.float64)
    Pulselist = np.linspace(0,nullLen-1,nullLen,dtype=int)
    variables = {"function":NullPulse,"Pulsewidth":nullLen}

    return packer(Pulselist, NullWfm, variables, [True, True], name="")

def packer(Pulsewidth, wave_amp, variables={}, appendRule=[False,False], name=""):
    """
    Returns
    -------
    properties : dict
        A dictionary of relavent data to be encapsulated.

    """
    properties = {
            'name': name,
            'variables': variables,
            'pulsewidth': Pulsewidth,
            'wave_amp': wave_amp,
            'appendRule': appendRule
            }
    return properties
