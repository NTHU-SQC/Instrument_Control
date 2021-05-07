import pyvisa as visa
import numpy as np
import time
# import a general instrument core by the method named absolute path import
from instruments.base.QEL_instrument_base import Instrument


class YokoGS200(Instrument):
    # check the class variable is a Private attribute.
    _rangeVOLT = {'30 V': 30E+0, '10 V': 10E+0,
                   '1 V': 1E+0, '100 mV': 100E-3, '10 mV': 10E-3}
    _rangeCURR = {'200 mA': 200E-3, '100 mA': 100E-3,
                   '10 mA': 10E-3, '1 mA': 1E-3}

    def __init__(self, inst_name, inst_visaAddress, dcState='CURRENT', timeout=5):
        super().__init__(inst_name, inst_visaAddress, timeout)
        self.__dcState = dcState

    def disconnect(self):
        '''
        When the GS200 is in remote mode
        the user can call this function to return it to local mode.
        '''
        self.inst.write(':SYSTem:LOCal')
        print(f'The instrument {self.instName} has been disconnected by YokoUSER.')
    
    def queryDCvalue(self):
        '''
        Get the present value of the dc source.
        '''
        print(self.inst.query('SOUR:LEV?'))

    def queryOutput(self):
        '''
        Get the output status
        '''
        print(self.inst.query(':OUTP?'))

    def setDCvalue(self, value:float):
        '''
        Set the present value of the dc source.
        '''
        self.inst.write(':SOUR:LEV ' + str(value))

    def setDCmode(self):
        '''
        This function can set the present status of DC mode 
        '''
        if self.__dcState.upper() in ('CURRENT', 'VOLTAGE'):
            command = ':SOUR:FUNC ' + self.__dcState
            self.inst.write(command)
        else:
            raise Exception('setDCmodeError! Please modify the Yoko object setting about dcState.')

    def setOutput(self, status:bool):
        '''
        This function can set the present status of Output
        status=0, it implies that YokoGS will turn off the output
        status=1, it implies that YokoGS will turn on the output
        '''
        command = ':OUTP ' + str(status)
        self.inst.write(command)

    def rangeLimit(self, rangeMode='1 V'):
        '''
        The protective mechanism for configuring DC value
        '''
        command = ':SOUR:RANG '

        if rangeMode in YokoGS200._rangeVOLT.keys() or \
            rangeMode in YokoGS200._rangeCURR.keys():
            if self.__dcState in ('CURRENT'):
                command = command + str(YokoGS200._rangeCURR[rangeMode])
            elif self.__dcState in ('VOLTAGE'):
                command = command + str(YokoGS200._rangeVOLT[rangeMode])

            # execute the above setting
            self.inst.write(command)
            print(f'\nrangeMode: "{rangeMode}", Setting completely!')

        else:
            if (rangeMode in YokoGS200._rangeVOLT.keys()) and \
                    (self.__dcState.upper() in 'CURRENT'):
                print(f'''Error message for "rangeLimit":
                          dcStateTypeError!
                          > Please check "rangeMode" is matched with "dcState"''')
            elif (rangeMode in YokoGS200._rangeCURR.keys()) and \
                    (self.__dcState.upper() in 'VOLTAGE'):
                print(f'''Error messagefor "rangeLimit":
                          dcStateTypeError!
                          > Please check "rangeMode" is matched with "dcState"''')
            else:
                print(f'''Error message for "rangeLimit":\n
                rangeModeTypeError!\n
                > You may want to type the following keywords in rangeMode.\n
                >>>>> The keyword of rangeVOLT: {YokoGS200._rangeVOLT.keys()}\n
                >>>>> The keyword of rangeCURR: {YokoGS200._rangeCURR.keys()}\n''')

    def _setRepeat(self, repeat:bool):
        command = ':PROG:REP ' + str(repeat)
        self.inst.write(command)

    def _setIntervalTime(self, IntervalTime):
        '''
        Range: from 0.1s to 3600.0s
        '''
        command = ':PROG:INT ' + str(IntervalTime)
        self.inst.write(command)

    def _setSlope(self, slopTime):
        '''
        Range: from 0.0s to 3600.0s
        '''
        command = ':PROG:SLOP ' + str(slopTime)
        self.inst.write(command)
    
    def sweepRate(self, sweepTime, intervalTime, repeat=0):
        '''
        set slope time and interval time with the same sweepTime
        '''
        self._setRepeat(repeat)
        self._setIntervalTime(intervalTime)
        self._setSlope(sweepTime)

    def sweepSlopeSetting(self, startPoint, endPoint):
        '''
        the value of startPoint is smaller than endPoint -> Rising
        the value of startPoint is larger than endPoint -> Falling  
        '''
        checkRangeLimit=str(self.inst.query(':SOUR:RANG?'))
        checkDCState=self.inst.query(':SOUR:FUNC?')

        startcmd = f':SOUR:FUNC {checkDCState};RANG {checkRangeLimit};LEV {startPoint}'
        endcmd = f':SOUR:FUNC {checkDCState};RANG {checkRangeLimit};LEV {endPoint}'

        self.inst.write(':PROG:EDIT:STAR')
        self.inst.write(startcmd)
        self.inst.write(endcmd)
        self.inst.write(':PROG:EDIT:END')
     
    def microwaveSwitch(self, sweepTime, intervalTime, startPoint, endPoint):
        '''
        Climb to a high point at a constant rate
        When climbing to a high point, stay for a fixed time
        Finally, gradually reduce the voltage value at the same rate until 0V
        '''
        print('\nStarting to execute the microwaveSwitch.')
		
        # Rising and waiting
        self.sweepRate(sweepTime, intervalTime)
        print('Rising Part.')
        self.sweepSlopeSetting(startPoint, endPoint)
        self.setOutput(status=1)
        self.inst.write(":PROG:RUN")
        print('Falling Part...')
        self.inst.write(":PROG:HOLD")
        self.sweepRate(sweepTime, intervalTime)
        
		# Falling and waiting
        self.sweepSlopeSetting(endPoint, startPoint)
        self.inst.write(":PROG:RUN")



if __name__ == "__main__":
    def main():
        '''
        Set a dc value pulse by doing a remote control
        Step 1. Connect the specific Yokogawa GS200 DC Voltage Current Source by adding a object named "YokoGS".
        Step 2. Attempt to do the remote connection of the "YokoGS",
                then you can see the below description in your terminal if the USB/GPIB plug-in has been connected to your computer correctly.
                Description:
                        Connect to YokoGS200 successfully
                        Statement: YOKOGAWA,GS210,91T810991,2.02
        Step 3. Set the DCmode in order to cover the previous setting.
        Step 4. Follow the below description.
                Description:
                        startPoint: Set the initial value
                        sweepTime: Climb to a high value at a fixed rate
                        waitTime: When climbing to a high point, stay for a fixed time
                        endPoint: Finally, gradually reduce the voltage value at the same rate until 0V
        '''
		pass
    