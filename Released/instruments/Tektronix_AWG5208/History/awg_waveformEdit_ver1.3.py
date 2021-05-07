
# -*- coding: utf-8 -*-
"""
Modified on Sat Nov 28 2020

@author: SQC_Lab, NTHU-SQC
@GitHub: sqclab225@gmail.com
@Maintainer: Ming Tze, Tzu Lu
"""
### import package 

import pyvisa as visa
import numpy as np
#from time import sleep
from datetime import datetime 
import time
import calendar
import matplotlib.pyplot as plt

### verify package version:
print('Numpy Version:', np.__version__)
#print('PyVISA Version:', visa.__version__)

### Initialization

### Instrument Communication
def updateAWG(name,wfmData,markerData,channel):
    recordLength=len(wfmData);

### Set up VISA intrument object
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, the timeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    print('Connect to ', awg.query('*idn?')) # comfirmation of the instrument

    #Send Waveform Data
    awg.write('WLIST:WAVEFORM:NEW "%s", %d' %(name, recordLength)) #create a new empty space for waveform data of same length
    stringArg = 'WLIST:WAVEFORM:DATA "{}", 0, {}, '.format(name, recordLength) #Fill the space created with 0 as initialization
    awg.write_binary_values(stringArg, wfmData) #Fill in the waveform data
    awg.write('*opc') #quering whether the intrument is pending.


   #Send Marker Data
    stringArg = 'wlist:waveform:marker:data "{}", 0, {}, '.format(name, recordLength) #Fill the space created with 0 as initialization 
    awg.write_binary_values(stringArg, markerData, datatype='B') #Fill in the Marker Data in Binary Form
    awg.write('*opc') #quering whether the intrument is pending.
    
    # Load waveform
    awg.write('SOURCE{}:CASSET:WAVEFORM "{}"'.format(channel,name))

    # Check for errors
    error = awg.query('system:error:all?')
    print('Status: {}'.format(error))

    awg.close() #Close the resource manager session
    
    
def clsTekWavSeq():
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    awg.write('SLIST:SEQUENCE:DELETE ALL')
    awg.write('WLISt:WAV:DEL ALL')
    print('Clean all')
    #Close the resource manager session
    awg.close()    

### Waveform Editting 

### Pulse Defining

### Gaussian Pulse (with Plateau) 

def gaussianPulse(sigma, flat):
    pulsewidth = flat + 6 * sigma+1
    wfmData = np.empty(pulsewidth, dtype=np.float64)
    tlist = np.linspace(0, pulsewidth-1, pulsewidth, dtype=int)
    peak= 3 * sigma;
    for i in range(len(tlist)):
    #(section 1)
        if(i <= peak):
            wfmData[i] = 1*np.exp(((-1*(tlist[i]-peak)**2)/(2*sigma**2)))
    #(section 2)
        elif( i > peak and i < peak+flat):
            wfmData[i] = 1
    #(section 3)
        else:
            wfmData[i] = 1*(np.exp((-1*(tlist[i]-flat-peak)**2)/(2*sigma**2)))
    return wfmData

### Square Pulse

def squarePulse(flattime):
    return np.ones(flattime)


### Waveform Delay

#*
def delayWaveform(wfmData,delay):
    return np.hstack((wfmData[-delay:],wfmData[-len(wfmData):-delay]))



def Sequence_Edit(total_length, qubit_seq,sigma_Q,flat_Q,sigma_C,flat_C,marker_durationQ,marker_durationC,marker_triggerC):

    ### Create waveform
    readout_seq  = total_length-qubit_seq

    #Qubit_sequence
    pulsewidth_Q = flat_Q + 6 * sigma_Q + 1 
    head    = qubit_seq - pulsewidth_Q
    tail    = readout_seq

    #delay = qubit_seq - flat_Q

    gaussian_Q = gaussianPulse(sigma_Q,flat_Q)
    noiseLv_head=np.zeros(head, dtype=np.float64)
    wfmData_Q=np.hstack((noiseLv_head,gaussian_Q))
    noiseLv_tail = np.zeros(tail, dtype=np.float64)
    wfmData_Q=np.hstack((wfmData_Q,noiseLv_tail))

    #Delay_waveform
    #wfmData = delayWaveform(wfmData,delay)


    #Readout_sequence
    pulsewidth_C = flat_C + 6 * sigma_C + 1
    relax_C  = readout_seq - pulsewidth_C
    on_hold_C =qubit_seq


    gaussian_C = gaussianPulse(sigma_C,flat_C)
    noiseLv_relax_C=np.zeros(relax_C, dtype=np.float64)
    wfmData_C=np.hstack((gaussian_C,noiseLv_relax_C))
    noiseLv_hold_C=np.zeros(on_hold_C,dtype=np.float64)
    wfmData_C=np.hstack((noiseLv_hold_C,wfmData_C))
    
    ### Create Marker
    #Qubit Marker
    sqflat_Q = squarePulse(marker_durationQ)
    #sqflat_Q = np.array((1<<7)*sqflat_Q,dtype=np.uint8)
    noiseLv_markerHeadQ = np.zeros(qubit_seq - marker_durationQ,dtype=np.float64)
    Marker_Q = np.hstack((noiseLv_markerHeadQ,sqflat_Q))
    noiseLv_markerTailQ = np.zeros(tail, dtype=np.float64)
    Marker_Q=np.hstack((Marker_Q,noiseLv_markerTailQ))
    Marker_Q = np.array((1<<7)*Marker_Q,dtype=np.uint8)
    #Marker_Q = np.array((1<<7)*np.ones(total_length),dtype=np.uint8)

    
    #Readout_Marker
    marker_onhold_C = qubit_seq + marker_triggerC
    marker_relaxC = total_length - marker_onhold_C - marker_durationC

    sqflat_C = squarePulse(marker_durationC)
    #sqflat_C = np.array((1<<7)*sqflat_C,dtype=np.uint8)
    noiseLv_markerHeadC = np.zeros(marker_onhold_C, dtype=np.float64)
    Marker_C = np.hstack((noiseLv_markerHeadC, sqflat_C))
    noiseLv_markerTailC = np.zeros(marker_relaxC, dtype=np.float64)
    Marker_C=np.hstack((Marker_C,noiseLv_markerTailC))
    Marker_C = np.array((1<<7)*Marker_C,dtype=np.uint8)
    #Marker_C = np.array((1<<7)*np.ones(total_length),dtype=np.uint8)


    #print(len(wfmData_Q))
    #print(len(wfmData_C))
    #print(len(Marker_Q))
    #print(len(Marker_C))


    #Nsample = range(0,total_length,1)
    
    #plt.plot(Nsample,wfmData_Q,Nsample,wfmData_C,Nsample,Marker_Q,Nsample,Marker_C,'r--')
    #plt.show()

    #sequence = [wfmData_Q,wfmData_C,Marker_Q,Marker_C]
    
    #return sequence
    
    ### Time Stamp for nonordering waveform (optional)
    
    timestamp = datetime.now()
    #timevalue=(timestamp.minute*60 + timestamp.second + (round(timestamp.microsecond/1000000,3))*1000)
    timevalue=(timestamp.minute*60 + timestamp.second + (round(timestamp.microsecond/1000000,3)))
    #timeRecord = str(int((timevalue)*1000))
    #timestamp = calendar.timegm(time.gmtime()) + (round(timestamp.microsecond/1000000,3))*1000
    timestamp = calendar.timegm(time.gmtime()) + timevalue*1000
    #timestamp = time.gmtime()
    timeRecord = str(int(timestamp))
    print(timeRecord)
    
    
    #Updatae waveform to AWG
    name_1 = "Gaussian_QubitDrive_" + str(flat_Q) + "ns_Series_"
    name_1 = name_1 + timeRecord
    updateAWG(name_1,wfmData_Q,Marker_Q,1)
    name_2 = "Gaussian_CavityDrive_" + str(flat_Q) + "ns_Series_"
    name_2 = name_2 + timeRecord
    updateAWG(name_2,wfmData_C,Marker_C,2)


total_length = 13752
qubit_seq    = 4250
sigma_Q = 100
flat_Q  = 0
sigma_C = 100
flat_C  = 2400
marker_durationQ = 0
marker_durationC = 200
marker_triggerC  = 100

#Sequence_Edit(total_length,qubit_seq,sigma_Q,flat_Q,sigma_C,flat_C,marker_durationQ,marker_durationC,marker_triggerC)


clsTekWavSeq()
### Load Waveform to AWG
#for i in range(600, -10, -10):
for i in range(0, 610, 10):
    Sequence_Edit(total_length,qubit_seq,sigma_Q,flat_Q+i,sigma_C,flat_C,marker_durationQ,marker_durationC,marker_triggerC)


### Test Draw Sequence Waveform
#Rabi_sequence = list()
#
#for i in range(0, 610, 10):
#    Rabi_sequence.append(Sequence_Edit(total_length,qubit_seq,sigma_Q,flat_Q+i,sigma_C,flat_C,marker_durationQ,marker_durationC,marker_triggerC))
#for i in range(61):
#    plt.clf()
#    Nsample = range(0,total_length,1)
#    plt.plot(Nsample,Rabi_sequence[i][0],Nsample,Rabi_sequence[i][1],Nsample,Rabi_sequence[i][2],Nsample,Rabi_sequence[i][3],'r--')
#    plt.savefig('Qubit_flat' + str(i*10) + 'nSample.png')
#
