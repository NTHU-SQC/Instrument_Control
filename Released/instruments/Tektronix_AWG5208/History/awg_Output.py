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


def Play():
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    awg.write('AWGControl:RUN') # CAUTION!: The sequence can only be played when it is loaded.\
   
    # Check for errors
    error = awg.query('system:error:all?')
    print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()
    
    
    
def Stop():
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    awg.write('AWGControl:STOP')
    
    # Check for errors
    error = awg.query('system:error:all?')
    print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()
    

def Channel_status(nCH, state = 'OFF'):
    rm = visa.ResourceManager()
    #awg = rm.open_resource('TCPIP0::192.168.20.43::inst0::INSTR') # Fill in the address of the instrument(AWG)
    awg = rm.open_resource( 'TCPIP0::169.254.146.217::inst0::INSTR')
    awg.timeout = 18000 #in pyVISA, ttimeout unit given in pyVISA is milliseconds by default.
    awg.write_termination = None
    awg.read_termination = '\n'
    
    # open: state 'ON' , close: state 'OFF'
    awg.write('OUTPut{}:STATe {}'.format(nCH, state))
    
    # Check for errors
    error = awg.query('system:error:all?')
    print('Status: {}'.format(error))
    
    #Close the resource manager session
    awg.close()
    

if __name__=='__main__':
    status = True
    
    #Channel_status(nCH=1,state = 'ON')
    #Play()
    #Stop()
    #Channel_status(nCH=1,state = 'OFF')
    
    
        


