from instruments.Tektronix_AWG5208.TektronixAWG_waveformEditor import Waveform 


class Time_Domain_Sequence(Waveform):
    # 20210402 Fri
    # TODO(CCvitaminHsieh): Need to add "Mistake-proofing" if the user type 
    #                       the unexpected arguments
    #                       (e.g. the value is out of range)in function,
    #                       it will remind the user that it raises some errors,
    #                       which arguments are in wrong or unexpected situation.
    #
    #
    #
    #
    def __init__(self):
        self._num_sigma = 3

    @property
    def num_sigma(self):
        print('getter of num_sigma called.')
        return self._num_sigma

    @num_sigma.setter
    def set_num_sigma(self, num_sigma:int):
        print('setter of num_sigma called.')
        self._num_sigma = num_sigma
        print('the variable "num_sigma" has been set to %d.'%(num_sigma))

    def store_wfmdata_properties(self, wfm_name, wfmData, mkrData, mkr_tone):
        """
        Descrition:

        Args:

        Example:

        """
        properties = {}

        properties['wfm_name'] = wfm_name
        properties['wfmData'] = wfmData
        properties['mkrData'] = mkrData
        properties['mkr_tone'] = mkr_tone

        return properties

    """
    Generate a time-domain-sequence with constraint conditions
    """
    def gen_gauss_wfmdata(self, wfm_name:str, wfm_totlen:int,wfm_offset:int,
                          gauss_sig: int, gauss_flat:int,
                          mkr_duration:int, mkr_tone:str)->str:
        """
        Descrition:

        Args:

        Example:

        """
        # The function can be used in "Rabi", "T1" situations with gaussian sharp
        # create a full waveform with marker data
        gauss_shape = self.gauss_square_pulse(gauss_sig,gauss_flat)    
        wfmData = self.waveform_shape(wfm_totlen, wfm_offset, gauss_shape)
        mkrData = self.marker_shape(wfm_totlen, wfm_offset, mkr_duration)                             
        wvname = wfm_name + '_GaussFlat_' + str(gauss_flat) + "pnts"

        
        result = self.store_wfmdata_properties(wvname, wfmData, mkrData, mkr_tone)
        return result
    
        # properties = {'wfm_name': wfm_name,
        #               'wfm_totlen': wfm_totlen,
        #               'wfm_offset': wfm_offset,
        #               'gauss_sig': gauss_sig,
        #               'mkr_duration': mkr_duration,
        #               'mkr_tone': mkr_tone}

        # return result, properties
        
    def _gen_T2_ramsey_wfmdata(self, wfm_name:str, wfm_totlen:int,
                             wfm_offset1:int, wfm_offset2:int,
                             gauss_sig:int, gauss_flat:int,
                             mkr_duration:int, mkr_tone:int)->str:
        """
        Descrition:

        Args:

        Example:

        """

        # create a full waveform with marker data
        gauss_shape = self.gauss_square_pulse(gauss_sig, gauss_flat)
        offset = (wfm_offset1, wfm_offset2)
        gauss_box = {'gauss1':gauss_shape, 'gauss2':gauss_shape}
        wfmData = self.multipulse_insert(wfm_totlen, *offset, **gauss_box)
        mkrData = self.marker_shape(wfm_totlen, wfm_offset2, mkr_duration)

        wvname = wfm_name + '_RamseyGaussFlat_' + str(gauss_flat) + "pnts"
        
        result = self.store_wfmdata_properties(wvname, wfmData, mkrData, mkr_tone)

        return result

    def _gen_T2_echo_wfmdata(self, wfm_name:str, wfm_totlen:int,
                           wfm_offset1:int, wfm_offset_m:int, wfm_offset2:int,
                           gauss_sig:int, gauss_flat:int, gauss_flat_med:int,
                           mkr_duration:int, mkr_tone:int)->str:
        """
        Descrition:

        Args:

        Example:

        """
        # create pi/2 pulse
        gauss_pi_div2 = self.gauss_square_pulse(gauss_sig,gauss_flat)
        # create pi pulse
        gauss_pi = self.gauss_square_pulse(gauss_sig,gauss_flat_med)                           
        # create a full waveform with marker data
        offset = (wfm_offset1, wfm_offset_m, wfm_offset2)
        gauss_box = {'gauss1': gauss_pi_div2,
                     'gauss_m':gauss_pi,
                     'gauss2':gauss_pi_div2}
        wfmData = self.multipulse_insert(wfm_totlen, *offset, **gauss_box)
        mkrData = self.marker_shape(wfm_totlen, wfm_offset2, mkr_duration)

        wvname = wfm_name + '_EchoGaussFlat_med_' + str(gauss_flat_med) + "pnts"

        result = self.store_wfmdata_properties(wvname, wfmData, mkrData, mkr_tone)

        return result

    def _gen_EIT_wfmdata(self, wfm_name:str, wfm_totlen:int,
                        wfm_offset1:int, wfm_offset2:int,
                        gauss_sig1:int, gauss_sig2:int,
                        gauss_flat1:int, gauss_flat2:int,
                        mkr_duration:int, mkr_tone:int)->str:
        """
        Descrition:

        Args:

        Example:

        """
        # create two different pulses
        p1_shape = self.gauss_square_pulse(gauss_sig1, gauss_flat1)
        p2_shape = self.gauss_square_pulse(gauss_sig2, gauss_flat2)
        # create a full waveform with marker data                     
        offset = (wfm_offset1, wfm_offset2)
        gauss_box = {'gauss1': p1_shape, 'gauss2':p2_shape}
        wfmData = self.multipulse_insert(wfm_totlen, *offset, **gauss_box)
        mkrData = self.marker_shape(wfm_totlen, wfm_offset2, mkr_duration)
        
        wvname = wfm_name + '_GaussFlat1_' + str(gauss_flat1) + \
                  '_GaussFlat2_' + str(gauss_flat2) +"pnts"
        
        result = self.store_wfmdata_properties(wvname, wfmData, mkrData, mkr_tone)

        return result
    
    
            

    def gen_Rabi_seq(self, gen_wfm_amount:int, wfm_totlen:int,
                    gauss_sig:int, gauss_delta_flat:int,
                    qb_mkr_duration:int, qb_mkr_tone:str,
                    rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                    rd_mkr_tone:str)->dict:
        """
        Descrition:

        Args:

        Example:

        """
        store_rabi_seq = {'QubitDrive':{}, 'ReadOut':{}}

        for i in range(gen_wfm_amount):
            qb_wfm_name = 'QubitDrive_Rabi_Index_' + str(i+1)
            qb_ft = i * gauss_delta_flat
            qb_gauss_len = 2 * self._num_sigma * gauss_sig \
                           + i * gauss_delta_flat
            qb_offset = rd_offset - qb_gauss_len
            rd_wfm_name = 'ReadOut_Rabi_Index_' + str(i+1) 

            no = i+1
            store_rabi_seq['QubitDrive'][no] = \
                                        self.gen_gauss_wfmdata(qb_wfm_name,
                                                                wfm_totlen,
                                                                qb_offset,
                                                                gauss_sig,
                                                                qb_ft, 
                                                                qb_mkr_duration,
                                                                qb_mkr_tone)
            
            store_rabi_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        
        return store_rabi_seq

    def gen_T1_seq(self, gen_wfm_amount:int,
                   wfm_totlen:int, gauss_sig:int,
                   qb_delay_delta:int, qb_flat:int,
                   qb_mkr_duration:int, qb_mkr_tone:str,
                   rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                   rd_mkr_tone:str)->dict:
        """
        Descrition:

        Args:

        Example:

        """
        store_T1_seq = {'QubitDrive':{}, 'ReadOut':{}}

        for i in range(gen_wfm_amount):
            qb_wfm_name = '%s_%d' %('QubitDrive_T1_Index_', i+1)
            qb_delay = i * qb_delay_delta
            qb_gauss_len = 2 * self._num_sigma * gauss_sig + qb_flat
            qb_offset = rd_offset - qb_delay - qb_gauss_len
            rd_wfm_name = '%s_%d_%s_%dpts' %('ReadOut_T1_Index',
                                            i+1,
                                            'delay',
                                            qb_delay)

            no = i+1
            store_T1_seq['QubitDrive'][no] = \
                                        self.gen_gauss_wfmdata(qb_wfm_name,
                                                                wfm_totlen,
                                                                qb_offset,
                                                                gauss_sig,
                                                                qb_flat, 
                                                                qb_mkr_duration,
                                                                qb_mkr_tone)
            
            store_T1_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        
        return store_T1_seq

    def gen_T2_ramsey_seq(self, gen_wfm_amount:int,
                          wfm_totlen:int, gauss_sig:int,
                          qb_delay_delta:int, qb_flat:int,
                          qb_mkr_duration:int, qb_mkr_tone:str,
                          rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                          rd_mkr_tone:str)->dict:
        """
        Descrition:

        Args:

        Example:

        """
        store_T2_ramsey_seq = {'QubitDrive':{}, 'ReadOut':{}}

        for i in range(gen_wfm_amount):
            qb_wfm_name = '%s_%d' %('QubitDrive_T2_ramsey_Index', i+1)
            qb_delay = i * qb_delay_delta
            qb_gauss_len = 2 * self._num_sigma * gauss_sig + qb_flat
            qb_offset_back = rd_offset - qb_gauss_len
            qb_offset_front = qb_offset_back - qb_delay - qb_gauss_len
            rd_wfm_name = '%s_%d_%s_%dpts' %('ReadOut_T2_ramsey_Index',
                                            i+1,
                                            'delay',
                                            qb_delay)

            no = i+1

            store_T2_ramsey_seq['QubitDrive'][no] = \
                                        self._gen_T2_ramsey_wfmdata(qb_wfm_name,
                                                                wfm_totlen,
                                                                qb_offset_front,
                                                                qb_offset_back,
                                                                gauss_sig,
                                                                qb_flat, 
                                                                qb_mkr_duration,
                                                                qb_mkr_tone)
            
            store_T2_ramsey_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        return store_T2_ramsey_seq

    def gen_T2_echo_seq(self, gen_wfm_amount:int,
                        wfm_totlen:int, gauss_sig:int,
                        qb_delay_delta:int,
                        qb_pi_div_by2_flat:int, qb_pi_flat:int,
                        qb_mkr_duration:int, qb_mkr_tone:str,
                        rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                        rd_mkr_tone:str)->dict:
        """
        Descrition:

        Args:

        Example:

        """                    
        store_T2_echo_seq = {'QubitDrive':{}, 'ReadOut':{}}

        for i in range(gen_wfm_amount):
            qb_wfm_name = '%s_%d' %('QubitDrive_T2_echo_Index', i+1)
            qb_pi_pulse_len = 2 * self._num_sigma * gauss_sig + qb_pi_flat 
            qb_pi_divby2_pulse_len = 2 * self._num_sigma * gauss_sig \
                                     + qb_pi_div_by2_flat

            qb_delay = i * qb_delay_delta
            qb_offset_back = rd_offset - qb_pi_divby2_pulse_len
            qb_offset_med = qb_offset_back - qb_pi_pulse_len - qb_delay
            qb_offset_front = qb_offset_med - qb_pi_divby2_pulse_len - qb_delay

            rd_wfm_name = '%s_%d_%s_%dpts' %('ReadOut_T2_echo_Index',
                                            i+1,
                                            'delay',
                                            qb_delay)

            no = i+1

            store_T2_echo_seq['QubitDrive'][no] = \
                                        self._gen_T2_echo_wfmdata(qb_wfm_name,
                                                                wfm_totlen,
                                                                qb_offset_front,
                                                                qb_offset_med,
                                                                qb_offset_back,
                                                                gauss_sig,
                                                                qb_pi_div_by2_flat,
                                                                qb_pi_flat, 
                                                                qb_mkr_duration,
                                                                qb_mkr_tone)
            
            store_T2_echo_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        return store_T2_echo_seq
    
    def gen_SPT_seq(self, gen_wfm_amount:int, wfm_totlen:int, gauss_sig:int,
                   qb_f12mkr_duration:int, qb_f12mkr_tone:str,
                   qb_t_tsdelta:int,
                   qb_f01mkr_duration:int, qb_f01mkr_tone:str,
                   rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                   rd_mkr_tone:str)->dict:
        """
        Description:
        
        Args:
        
        Example:
        
        """
        qb_f01flat = 0
        qb_f12flat = 0
        
        
        store_SPT_seq = {'QubitDrive_f12':{}, 'QubitDrive_f01':{}, 'ReadOut':{}}
        
        for i in range(gen_wfm_amount):
            qb_f01wfm_name = 'QubitDrive_f01_Index_' + str(i+1) 
            qb_f01_pulsewidth = 2 * self._num_sigma * gauss_sig
            qb_f01_offset = rd_offset - qb_f01_pulsewidth
            
            qb_delay = i * qb_t_tsdelta 
            qb_f12wfm_name = 'QubitDrive_f12_Index_' + str(i+1) 
            qb_f12_offset = rd_offset - qb_f01_pulsewidth - qb_delay
            
            rd_wfm_name = 'ReadOut_Index_' + str(i+1)
            no = i + 1 
            
            store_SPT_seq['QubitDrive_f01'][no] = \
                                        self.gen_gauss_wfmdata(qb_f01wfm_name,
                                                                wfm_totlen,
                                                                qb_f01_offset,
                                                                gauss_sig,
                                                                qb_f01flat, 
                                                                qb_f01mkr_duration,
                                                                qb_f01mkr_tone)
            store_SPT_seq['QubitDrive_f12'][no] = \
                                        self.gen_gauss_wfmdata(qb_f12wfm_name,
                                                                wfm_totlen,
                                                                qb_f12_offset,
                                                                gauss_sig,
                                                                qb_f12flat, 
                                                                qb_f12mkr_duration,
                                                                qb_f12mkr_tone)
            
            store_SPT_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        
        return store_SPT_seq 

    def gen_EIT_seq(self, gen_wfm_amount:int,
                    wfm_totlen:int, delay_time_delta:int,
                    qb_gauss_sig_front:int, qb_gauss_sig_back:int,
                    qb_gauss_flat_front:int, qb_gauss_flat_back:int,
                    qb_mkr_duration:int, qb_mkr_tone:str,
                    rd_gauss_sig:int, rd_offset:int, rd_flat:int,
                    rd_mkr_duration:int, rd_mkr_tone:str)->dict:
        """
        Descrition:

        Args:

        Example:

        """
        store_EIT_seq = {'QubitDrive':{}, 'ReadOut':{}}

        for i in range(gen_wfm_amount):
            qb_wfm_name = '%s_%d' %('QubitDrive_EIT_Index', i+1)
            qb_gauss_pulse_front_len = 2 * self._num_sigma * qb_gauss_sig_front \
                                       + qb_gauss_flat_front
            qb_gauss_pulse_back_len = 2 * self._num_sigma * qb_gauss_sig_back \
                                       + qb_gauss_flat_back

            qb_delay = i * delay_time_delta

            qb_eit_offset_back = rd_offset - qb_gauss_pulse_back_len
            qb_eit_offset_front =  qb_eit_offset_back \
                                   - qb_delay - qb_gauss_pulse_front_len

            rd_wfm_name = '%s_%d_%s_%dpts' %('ReadOut_EIT_Index',
                                             i+1,
                                             'delay',
                                             delay_time_delta)

            no = i+1

            store_EIT_seq['QubitDrive'][no] = \
                                    self._gen_EIT_wfmdata(qb_wfm_name,
                                                         wfm_totlen,
                                                         qb_eit_offset_front,
                                                         qb_eit_offset_back,
                                                         qb_gauss_sig_front,
                                                         qb_gauss_sig_back,
                                                         qb_gauss_flat_front,
                                                         qb_gauss_flat_back,
                                                         qb_mkr_duration,
                                                         qb_mkr_tone)
            
            store_EIT_seq['ReadOut'][no] = \
                                    self.gen_gauss_wfmdata(rd_wfm_name,
                                                          wfm_totlen, 
                                                          rd_offset, 
                                                          rd_gauss_sig,
                                                          rd_flat,
                                                          rd_mkr_duration, 
                                                          rd_mkr_tone)
        return store_EIT_seq
    
    def gen_SPTrabi_seq(self, gen_wfm_amount:int, wfm_totlen:int,
                    gauss_sig:int, qb_f12_delta_flat:int,
                    qb_f12mkr_duration:int, qb_f12mkr_tone:str,
                    qb_f01_pumping_pi:int,
                    qb_f01mkr_duration:int, qb_f01mkr_tone:str,
                    rd_offset:int, rd_flat:int, rd_mkr_duration:int,
                    rd_mkr_tone:str)->dict:
        """
        Description:
        
        Args:
        
        Example:
        
        """
        
        store_SPTrabi_seq = {'QubitDrive_f12':{}, 'QubitDrive_f01':{}, 'ReadOut':{}}
        
        for i in range(gen_wfm_amount):
            qb_f12wfm_name = 'QubitDrive_f12_Rabi_Index_' + str(i+1)
            qb_f12flat = i * qb_f12_delta_flat
            qb_f12_pulsewidth = 2 * self._num_sigma * gauss_sig \
                                + qb_f12flat
            qb_f12_offset = rd_offset - qb_f12_pulsewidth
            qb_f01wfm_name = 'QubitDrive_f01_Pumping_Index_' + str(i+1)
            qb_f01_pulsewidth = 2 * self._num_sigma * gauss_sig \
                                + qb_f01_pumping_pi
            qb_f01_offset = rd_offset - qb_f12_pulsewidth - qb_f01_pulsewidth
            rd_wfm_name = 'ReadOut_Rabi_Index_' + str(i+1)
            no = i + 1 
            
            store_SPTrabi_seq['QubitDrive_f12'][no] = \
                                        self.gen_gauss_wfmdata(qb_f12wfm_name,
                                                                wfm_totlen,
                                                                qb_f12_offset,
                                                                gauss_sig,
                                                                qb_f12flat, 
                                                                qb_f12mkr_duration,
                                                                qb_f01mkr_tone)
            store_SPTrabi_seq['QubitDrive_f01'][no] = \
                                        self.gen_gauss_wfmdata(qb_f01wfm_name,
                                                                wfm_totlen,
                                                                qb_f01_offset,
                                                                gauss_sig,
                                                                qb_f01_pumping_pi, 
                                                                qb_f01mkr_duration,
                                                                qb_f01mkr_tone)
            
            store_SPTrabi_seq['ReadOut'][no] = \
                                     self.gen_gauss_wfmdata(rd_wfm_name,
                                                            wfm_totlen, 
                                                            rd_offset, 
                                                            gauss_sig,
                                                            rd_flat,
                                                            rd_mkr_duration, 
                                                            rd_mkr_tone)
        
        return store_SPTrabi_seq 
    

    def decorate2seq_format(self):
        """
        Descrition:

        Args:

        Example:

        """
        pass

if __name__=='__main__':
    import pprint as pp
    import matplotlib.pyplot as plt

    """
    Create an object to build a sequence for time-domain experiments
    """
    test = Time_Domain_Sequence()
    """
    Get the more details of the object named Sequence by the function named Help
    """
    # help(Sequence())
    """ 
    Generate a waveform with a single gaussian
    """
    # result = test.gen_gauss_wfmdata('gaussian', 
    #                                 10000,
    #                                 1000,
    #                                 100,
    #                                 1000,
    #                                 0,
    #                                 'mkr1')
    # x = [i for i in range(len(result['wfmData']))]
    # plt.plot(x, result['wfmData'])
    # plt.show()
    # pp.pprint(result)                                                              
    """
    Generate a rabi-sequence with several variety of waveforms
    """
    # wfm_amount = 10
    # wfm_totlen = 10000
    # gauss_sig = 100
    # gauss_delta_flat = 200
    # qubitDrive_mkrDuration = 0
    # qubitDrive_mkr = 'no_mkr'

    # readOut_offset = 5000
    # readOut_flat = 2400
    # readOut_mkrDuration = 200
    # readOut_mkr = 'mkr1'
    
    # store_rabi_seq = {}

    # store_rabi_seq = test.gen_Rabi_seq(wfm_amount,
    #                                     wfm_totlen,
    #                                     gauss_sig,
    #                                     gauss_delta_flat,
    #                                     qubitDrive_mkrDuration,
    #                                     qubitDrive_mkr,
    #                                     readOut_offset,
    #                                     readOut_flat,
    #                                     readOut_mkrDuration,
    #                                     readOut_mkr)
    # pp.pprint(store_rabi_seq)
    """
    Generate a T1-sequence with several variety of waveforms
    """
    # wfm_amount = 10
    # wfm_totlen = 10000
    # gauss_sig = 100
    
    # qubitDrive_delay_time_delta = 100
    # qubitDrive_flat = 80
    # qubitDrive_mkrDuration = 0
    # qubitDrive_mkr = 'no_mkr'

    # readOut_offset = 4000
    # readOut_flat = 2400
    # readOut_mkrDuration = 200
    # readOut_mkr = 'mkr1'
    
    # store_t1_seq = {}

    # store_t1_seq = test.gen_T1_seq(wfm_amount,
    #                                 wfm_totlen,
    #                                 gauss_sig,
    #                                 qubitDrive_delay_time_delta,
    #                                 qubitDrive_flat,
    #                                 qubitDrive_mkrDuration,
    #                                 qubitDrive_mkr,
    #                                 readOut_offset,
    #                                 readOut_flat,
    #                                 readOut_mkrDuration,
    #                                 readOut_mkr)
    # pp.pprint(store_t1_seq)
    """
    Generate a T2-ramsey-sequence with several variety of waveforms
    """
    # wfm_amount = 10
    # wfm_totlen = 10000
    # gauss_sig = 100
    
    # qubitDrive_delay_time_delta = 50
    # qubitDrive_flat = 60
    # qubitDrive_mkrDuration = 0
    # qubitDrive_mkr = 'no_mkr'

    # readOut_offset = 6000
    # readOut_flat = 2400
    # readOut_mkrDuration = 200
    # readOut_mkr = 'mkr1'
    
    # store_t2_ramsey_seq = {}

    # store_t2_ramsey_seq = test.gen_T2_ramsey_seq(wfm_amount,
    #                                             wfm_totlen,
    #                                             gauss_sig,
    #                                             qubitDrive_delay_time_delta,
    #                                             qubitDrive_flat,
    #                                             qubitDrive_mkrDuration,
    #                                             qubitDrive_mkr,
    #                                             readOut_offset,
    #                                             readOut_flat,
    #                                             readOut_mkrDuration,
    #                                             readOut_mkr)
    # pp.pprint(store_t2_ramsey_seq)
    """
    Generate a T2-echo-sequence with several variety of waveforms
    """
    # wfm_amount = 10
    # wfm_totlen = 10000
    # gauss_sig = 100
    
    # qubitDrive_delay_time_delta = 200
    # qubitDrive_flat_pi_divby2 = 58
    # qubitDrive_flat_pi = 80
    # qubitDrive_mkrDuration = 0
    # qubitDrive_mkr = 'no_mkr'

    # readOut_offset = 6000
    # readOut_flat = 2400
    # readOut_mkrDuration = 200
    # readOut_mkr = 'mkr1'
    
    # store_T2_echo_seq = {}

    # store_T2_echo_seq = test.gen_T2_echo_seq(wfm_amount,
    #                                             wfm_totlen,
    #                                             gauss_sig,
    #                                             qubitDrive_delay_time_delta,
    #                                             qubitDrive_flat_pi_divby2,
    #                                             qubitDrive_flat_pi,
    #                                             qubitDrive_mkrDuration,
    #                                             qubitDrive_mkr,
    #                                             readOut_offset,
    #                                             readOut_flat,
    #                                             readOut_mkrDuration,
    #                                             readOut_mkr)
    # pp.pprint(store_T2_echo_seq)
    """
    Generate an EIT-sequence with several variety of waveforms
    """
    """
    wfm_amount = 2
    wfm_totlen = 10000
    gauss_sig = 100
    
    qubitDrive_delay_time_delta = 40
    qubitDrive_gauss_sig_front = 100
    qubitDrive_gauss_flat_front = 300
    qubitDrive_gauss_sig_back = 100
    qubitDrive_gauss_flat_back = 100
    qubitDrive_mkrDuration = 0
    qubitDrive_mkr = 'no_mkr'
    
    readOut_sigma = 100
    readOut_offset = 6000
    readOut_flat = 2400
    readOut_mkrDuration = 200
    readOut_mkr = 'mkr1'
    
    store_EIT_seq = {}

    store_EIT_seq = test.gen_EIT_seq(wfm_amount,
                                        wfm_totlen,
                                        qubitDrive_delay_time_delta,
                                        qubitDrive_gauss_sig_front,
                                        qubitDrive_gauss_sig_back,
                                        qubitDrive_gauss_flat_front,
                                        qubitDrive_gauss_flat_back,
                                        qubitDrive_mkrDuration,
                                        qubitDrive_mkr,
                                        readOut_sigma,
                                        readOut_offset,
                                        readOut_flat,
                                        readOut_mkrDuration,
                                        readOut_mkr)
    
    pp.pprint(store_EIT_seq)

    for track in tuple(store_EIT_seq.keys()):
        print(track)
        for step in store_EIT_seq[track].keys():
            print('step: {}'.format(step))
            print('wfm_name: ', store_EIT_seq[track][step]['wfm_name'])
            print('wfmData', store_EIT_seq[track][step]['wfmData'])
            print('mkrData', store_EIT_seq[track][step]['mkrData'])
            print('mkr_tone', store_EIT_seq[track][step]['mkr_tone'])
            if step == tuple(store_EIT_seq[track].keys())[-1]:
                print('last step: ', step)
   """