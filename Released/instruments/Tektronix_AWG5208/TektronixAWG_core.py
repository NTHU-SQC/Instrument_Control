# -*- coding: utf-8 -*-
# Reference: https://download.tek.com/manual/AWG5200-Programmer-Manual-077133700.pdf
import numpy as np
import pyvisa as visa
from time import sleep
from instruments.base.QEL_instrument_base import Instrument


class Tektronix_AWG5208(Instrument):
    def __init__(self, inst_name:str, inst_visaAddress:str, timeout:int=18000):
        """
        For example,
        Once the user create a object,
        the program will attemp to build a connection 
        between this PC and Tektronix AWG 5208 
        via TCP/IP protocol.
        
        The arguments are required to follow the syntax.
        inst_name: 'Tektronix_AWG_5208'
        inst_visaAddress: 'TCPIP0::192.168.20.43::inst0::INSTR'
        timeout: 18000(sec)
        marked
        """
        super().__init__(inst_name, inst_visaAddress, timeout)
        self._MKR_PARAM = {'mkr1':128, 'mkr2':64,'mkr3':32, 'mkr4':16,
                            'no_mkr':1}


    def check_awg_error(self):
        """
        Description:
            Returns the error and event query for all the unread items 
            and removes them from the query.
        marked
        """
        print('AWG Status: %s' %(self.inst.query('system:error:all?')))

    def awg_play(self):
        """
        Description:
            Initiates the channel output of a waveform or sequence.
        marked
        """
        self.inst.write('AWGControl:RUN')

    def awg_stop(self):
        """
        Description:
            Stops the output of a waveform or sequence
        marked
        """
        self.inst.write('AWGControl:STOP')

    def set_sample_rate(self, sample_rate:float=1.0E9):
        """
        Description:
            Sets the output sampling rate for these channel signals.
        Args:
            sample_rate: the sampling rate and the the rate range is 
                  		 from 298S/s to 2.5G/s.(option 25)
        Example:
            set_sample_rate(1.0E9)

            The function will set the output sampling rate to 1.0 GS/s
        marked
        """
        self.inst.write('CLOCk:SRATe %d' %(int(sample_rate)))

    def set_extref_source(self, ref_freq:int=10E6):
        """
        Description:
            Setting Clock/Reference sources in AWG_Clock panel 
        Args:
            ref_freq: a reference frequency at the Reference In connector.
        Example:
            1. set_extref_source(ref_freq=10E6)
               When the value of ref is 10E6, indicating that 
               the reference frequency is set a fixed 10 MHz reference source.

            2. set_extref_source(ref_freq=5E6)
               When the value of ref is 5E6, indicating that 
               the reference frequency is set a variable(5MHz) reference source.
        marked
        """
        
        if ref_freq == 10E6:
            status = 'EFIXed'
        else:
            status = 'EVAR' + str(int(ref_freq))

        self.inst.write('AWGControl:CLOCk:SOURce %s' %(status))

    def set_channel_mkr(self, ch_mkr1=0, ch_mkr2=1, ch_mkr3=0, ch_mkr4=0,
                              ch_mkr5=0, ch_mkr6=0, ch_mkr7=0, ch_mkr8=0):
        """
        Description:
            There are 8 channels in AWG5208. Each with 4 markers at most, 0 at least.
            Each channel has 16 bits resolution. One additional mkr occupies 1 bit,
            Therefore, reducing 1 bit resolution. e.g 16 + 0 Mkr -> 15 + 1 Mkr
        Args:
            ch_mkr[n]: The user can open the number of markers from 0 to 4.
                       n: The specific channel
        Example:
            set_channel_mkr(1, 1, 0, 0, 0, 0, 0, 0)

            Only the marker of Channel 1 and Channel 2 will be set to 1, 
            the others will be set to 0.
        marked
        """
        self.marker_status = {'marker_1': ch_mkr1,
        					  'marker_2': ch_mkr2,
                              'marker_3': ch_mkr3,
                              'marker_4': ch_mkr4,
                              'marker_5': ch_mkr5,
                              'marker_6': ch_mkr6,
                              'marker_7': ch_mkr7,
                              'marker_8': ch_mkr8}
        
        resolution_bit = 16
        
        for ch_status, ch_mkr in enumerate(self.marker_status.values()):
            mkr_num = resolution_bit - ch_mkr
            command = 'SOURce{}:DAC:RESolution {};' .format(ch_status+1, mkr_num)
            self.inst.write(command)
            sleep(0.001)

    def send_wfm_to_wlist(self, wfm_name: str, wfm_length: int, wfm_data: list):
        """
        Description:
            Upload waveform data to Waveform List
        Args:
            wfm_name: the name of the waveform 
            wfm_length: the total length of the waveform
            wfm_data: the content of the waveform stored in *list* type
        Example:
			send_wfm_to_awg('GaussPulse', 10000, GaussPulseArr)

			When the user calls the function, it will generate a new array
			named 'GaussPulse' with the length of 10000 zero elements as init, and
			fill in the pre-designed pts(GaussPulseArr) in 'GaussPulse'.

        marked
        """
        # create a new empty space for waveform data of same length
        self.inst.write('WLIST:WAVEFORM:NEW "%s", %d' %(wfm_name, wfm_length))
        # fill the space created with "0" as initialization
        # then store the waveform data
        stringArg = 'WLIST:WAVEFORM:DATA "%s", 0, %d, ' %(wfm_name, wfm_length)
        self.inst.write_binary_values(stringArg, wfm_data)
        # quering whether the intrument is pending
        self.inst.write('*opc')

    def send_mkr_to_wfm(self, wfm_name:str, wfm_length:int, mkr_data:list):
        """
        Description:
            Upload the marker data to the specified waveform 
        Args:
            wfm_name: the name of the waveform 
            wfm_length: the total length of the waveform
            mkr_data: the content of the waveform stored in *list* type
        Example:
            send_mkr_to_wfm("SineWave", 10000, SineArr)

            It will send the marker data to the waveform named "SineWave"
            if the list named SineArr is pre-defined.
        marked
        """
        # page 370 in AWG5200 Series Arbitrary Waveform Generators Programmer

        # fill the space created with 0 as initialization
        # then fill in the marker data in Binary type
        stringArg = 'wlist:waveform:marker:data "{}", 0, {}, '.format(wfm_name,
        														      wfm_length)
        self.inst.write_binary_values(
                            stringArg,
                            np.array(mkr_data, dtype=np.uint8),
                            datatype='B')
        # Quering whether the intrument is pending
        self.inst.write('*opc')

    def get_mkr_tone_param(self):
        """
        Description:
            
        """
        print(self._MKR_PARAM)

    def send_wfmData_withmkr2AWG(self, wfm_name, wfmData, mkrData, mkr_tone):
        """
        Description:
        Args:
        """
        # send a wfmData to WaveformList
        self.send_wfm_to_wlist(wfm_name, len(wfmData), wfmData)
        # let the specified waveform with mkrData
        if mkr_tone in self._MKR_PARAM.keys():
            mkr_select = self._MKR_PARAM[mkr_tone]
            self.send_mkr_to_wfm(wfm_name, len(wfmData),
                                mkr_select*np.array(mkrData))
        else:
            pass

    def load_wfm_to_channel(self, channel:int, wfm_name:str):
        """
        Description:
            Assign a waveform from the waveform list to the specified channel.
        Args:
            channel: the specified channel
            wfm_name: the name of the waveform
        Example:
            load_wfm_to_channel(1, "SineWave")

            The function will assign a waveform named "SineWave" 
            from the Waveform List to Channel 1.
        """        
        self.inst.write('SOURCE{}:CASSET:WAVEFORM "{}"'.format(channel,
                                                               wfm_name))

    def seq_table_creator(self, seq_name:str='SeqSample', 
                                seq_step=61, seq_num_track=2):
        """
        Description:
            The function can create a new sequence with the defined name, 
            the number of step, and number of tracks.
        Args:
            seq_name: assign a name to the new sequence
            seq_step: the total steps of a new sequence
                        (1 <= SeqTotStep <= 16383)
            seq_num_track: the total tracks of a new sequence
                      (1 <= NumTrack <= 8)
        Example:
            seq_table_creator("Rabi_Sequence", 20, 2)

            The function will create a empty sequence with 20 steps and 2 tracks.
        """
        command = 'SLISt:SEQuence:NEW "{}",{},{}'.format(seq_name,
                                                         seq_step,
                                                         seq_num_track)
        self.inst.write(command)

    def wfm_assign_to_seq(self, seq_name:str, wfm_name:str,
                                seq_track_index:int, seq_step_index:int):
        """
        Description:
            Assign a waveform for a specific sequence's step and track.
        Args:
            seq_name: the name of sequence 
            wfm_name: select the specified waveform from Waveform List
            seq_track_index: insert the waveform to the specified track
            seq_step_index: insert the waveform to the specified step
        Example:
            wfm_assign_to_seq("Rabi_Sequence", "Readout_Pulse", 2, 1)

            After creating a empty sequence named "Rabi_Sequence"
            with the function called *seq_table_creator*, 
            the user can execute the above function 
            to assign the waveform named "Readout_Pulse" to the step 1 of the track 2
            of the sequence named "Rabi_Sequence" 
        marked
        """
        
        command = 'SLISt:SEQuence:STEP{}:TASSet{}:WAVeform "{}","{}"'.format(
        				seq_step_index, seq_track_index, seq_name, wfm_name)
        self.inst.write(command)

    def load_seq_to_channel(self, channel:int, seq_name:str, seq_track_index:int):
        """
        Description:
            Assign a track of sequence to the specific channel
        Args:
            channel: the number of the specified channel
            seq_name: the name of sequence in Sequence List
            seq_track_index: track number
        Example:
            load_seq_to_channel(2, "Rabi_Sequence", 2)

            It impies that it will assign track 2 of "Rabi_Sequence" to Channel 2
        marked
        """        
        command = 'SOURCE{}:CASSET:SEQUENCE "{}", {}'.format(channel,
                                                             seq_name,
                                                             seq_track_index)
        self.inst.write(command)

    def seq_step_goto(self, seq_name, step, target):
        """
        Description:
            Set the target step for the GOTO command of the sequencer
            at the specified step.
        Args:
            seq_name: the name of sequence
            step: value specifying a sequence step
            target:
                n: repeat the specified step to play n times
                   where the value of n is between 1 and 16383.
                LAST: let the specified step go to the last step
                      in the sequence.
                FIRST: let the specified step go to the first step
                      in the sequence.
                NEXT: let the specified step go to the next step
                      in the sequence.
                END: let the sequence go to the end and play 0 V
                     until play is stopped.
        """
        command = 'SLISt:SEQuence:STEP'

        if target.upper() in ('LAST', 'FIRST', 'NEXT', 'END'):
            target = target.upper()
        elif 1 <= target <= 16383:
            target = target
        else:
            target = None

        if target != None:    
            command = 'SLISt:SEQuence:STEP{}:GOTO "{}", {}'.format(step,
                                                                   seq_name,
                                                                   target)
            self.inst.write(command)
        else:
            print('do nothing')
        
    def seq_step_repeat_count(self, seq_name, step, count):
        """
        Description:
            Set the repeat count,
            which is the number of times the assigned waveform(s) play
            before proceeding to the next step in the sequence.
        Args:
            seq_name: the name of sequence
            step: value specifying a sequence step
            count:
                ONCE: plays the waveform one time during this sequence step.
                INF: plays the waveform continuously during this sequence step.
                n: play the waveform the selected number of times 
                   during this sequence step. 
                   The allowed value is between 1 and 2^32-1
        """
        if count.upper() in ('ONCE', 'INF'):
            count = count.upper()
        elif 1 <= count <= 2**32-1:
            count = count
        else:
            count = None
        
        if count != None:
            command = 'SLISt:SEQuence:STEP{}:RCOunt "{}", {}'.format(step,
                                                                     seq_name,
                                                                     count)
            self.inst.write(command)
        else:
            print('do nothing')

    def set_sequential_assign_wfm2seqtable(self, seq_name:str,
                                           track_assign_order:list,
                                           seq_data_dict:dict):
        #TODO
        seq_step = len(seq_data_dict[track_assign_order[0]].keys())
        seq_num_track = len(track_assign_order)
        self.seq_table_creator(seq_name, seq_step, seq_num_track)
        track_assign_order = list(track_assign_order)
        try:
            for track_index, track in enumerate(track_assign_order):
                step_set = seq_data_dict[track].keys()
                for step_index, step in enumerate(step_set):
                    properties = seq_data_dict[track][step]
                    self.send_wfmData_withmkr2AWG(properties['wfm_name'],
                                                  properties['wfmData'],
                                                  properties['mkrData'],
                                                  properties['mkr_tone'])
                    self.inst.write('*opc')
                    self.wfm_assign_to_seq(seq_name,
                                           properties['wfm_name'],
                                           track_index+1,
                                           step_index+1)
                    if step_index+1 == tuple(step_set)[-1]:
                        self.seq_step_goto(seq_name, step_index+1, 'FIRST')
                        self.inst.write('*opc')
                    self.inst.write('*opc')
                    sleep(0.001)
            print('The transfer mission is completed.')
        except Exception as err_message:
            print(err_message)
        
            


    def del_wlist(self):
        """
        Description:
            Delete all waveforms from the Waveform List
        marked
        """
        self.inst.write('WLISt:WAVeform:DELete ALL')

    def del_slist(self):
        """
        Description:
            Delete all sequences from the Sequence List
        marked
        """
        self.inst.write('SLISt:SEQuence:DELete ALL')




if __name__ == '__main__':
    pass