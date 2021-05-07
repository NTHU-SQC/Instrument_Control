"""
Modified on Sat Nov 28 2020

@author: SQC_Lab, Hoiqel
@GitHub: sqclab225@gmail.com
@Maintainer: Ming Che, Tzu Lu
"""
### import package 
import pyvisa as visa
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
import re
import copy

### verify package version:
#print('Numpy Version:', np.__version__)
#print('PyVISA Version:', visa.__version__)

### Initialization

### Instrument Communication 
def clsTekSeq(delname='ALL'):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    if delname == 'ALL':
        awg.write('SLIST:SEQUENCE:DELETE ALL')
    else:
        awg.write('SLIST:SEQUENCE:DELETE "{}"'.format(delname))
    
    #error = awg.query('system:error:all?')
    #print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()

    
def scanWF(KEYWORD='Gaussian'):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    # List all waveforms in WaveformList by using Regular Expression
    AllWFList = awg.query('WLISt:LIST?').replace(',', ' ')
    pattern = r"\b%s\S*\b" %(KEYWORD)
    ReAllWFList = re.findall(pattern, AllWFList)
    
    #Close the resource manager session
    awg.close() 
    
    return ReAllWFList

def SortWFList(WFList):
    #print(WFList)
    TimeorderList = list()
    NewWFList  = list()    
    pattern = re.compile(r"\d\d\d\d\d\d\d\d\d\d")
    #pattern = re.compile(r"\d+")
    for i in range(len(WFList)):
        TimeorderList.append(re.findall(pattern,WFList[i])[0])   
   
    TimeorderSet=set(TimeorderList)
    TimeorderList = list(TimeorderSet)
    TimeorderList.sort()
    
    for i in range(len(TimeorderList)):
        label = TimeorderList[i]
        #print('index[{}]:{} vs WFList[{}]:{}\n'.format(i, label, i, WFList[i]))
        for j in range(len(WFList)):
            if label in WFList[j]:
                NewWFList.append(WFList[j])
    
    #for i in range(len(NewWFList)):
    #    NewWFList[i] = NewWFList[i][:-18]
    
    
    #print(NewWFList)
    return NewWFList                    
    
   
       
def wavGroup(WaveformList, label='CavityDrive'):
    wavList = list()
    for i in range(len(WaveformList)):
        if label in WaveformList[i]:
            wavList.append(WaveformList[i])
    return wavList
    
def seqCreate(TotStep, wfmName='SeqQubitDrive', Ntrack=2):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    #sequence parameters
    awg.write('SLISt:SEQuence:NEW "{}",{},{}'.format(wfmName, TotStep, Ntrack))
    
    # Check for errors
    error = awg.query('system:error:all?')
    print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()
    
def seqAssign(StepN=1, trackN=1, seqName='SeqQubitDrive', wavName='Gaussian_QubitDrive_0ns'):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    # Assign waveform
    awg.write('SLISt:SEQuence:STEP{}:TASSet{}:WAVeform "{}","{}"'.format(StepN, trackN, seqName, wavName))
    
    # Check for errors
    #error = awg.query('system:error:all?')
    #print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()
    
def seqMakeTable(WavListCavity, WavListQubit, seqName='SeqQubitDrive'):
    for StepN in range(1, len(wavListCavity) + 1):
        for trackN in range(1,2 + 1):
            if trackN % 2 == 1:
                seqAssign(StepN, trackN, seqName, wavName=wavListQubit[StepN - 1])
            else:
                seqAssign(StepN, trackN, seqName, wavName=wavListCavity[StepN - 1])
                
def seqFinalStepToFirst(FinalStep, seqName):       
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    awg.write('SLISt:SEQuence:STEP{}:GOTO "{}", {}'.format(FinalStep, seqName, "FIRSt"))
    
    #Close the resource manager session
    awg.close()

def LoadSeqToChannel(Channel, seqName, trackN):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    awg.write('SOURCE{}:CASSET:SEQUENCE "{}", {}'.format(Channel, seqName, trackN))
    
    awg.close()
    
def debugQQ():
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    print(awg.query('WLISt:LIST?'))
    
    awg.close()
    
if __name__=='__main__':
    
    WavList = scanWF()
    WavList = SortWFList(WavList)
    wavListCavity = wavGroup(WavList, label='CavityDrive')
    wavListQubit = wavGroup(WavList, label='QubitDrive')
    
    
    clsTekSeq()
    seqCreate(TotStep=len(wavListCavity))
    seqAssign()
    seqMakeTable(wavListCavity, wavListQubit)
    seqFinalStepToFirst(FinalStep=len(wavListCavity), seqName='SeqQubitDrive')
    
    # TrackN=1: QubitTone
    # TrackN=2: CavityTone
    LoadSeqToChannel(Channel=1, seqName='SeqQubitDrive', trackN=1)
    LoadSeqToChannel(Channel=2, seqName='SeqQubitDrive', trackN=2)
    
    #debugQQ()