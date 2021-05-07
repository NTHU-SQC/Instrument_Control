# -*- coding: utf-8 -*-
import pyvisa as visa
from time import sleep


class Instrument:
    def __init__(self, inst_name='',
                 inst_visaAddress='GPIB0::1::INSTR',
                 timeout=5):
        """
        Once the user create a object,
        the object will attempt to build a connection
        between this PC and your instrument.

        1.  
        reading self-identification for Yokogawa GS200
        with GPIB number 1.
        The arguments are required to follow the syntax.
        inst_name = 'YokoDC'
        get_address = 'GPIB0::1::INSTR'
        timeout: 5(sec)

        2.
        reading self-identification for Tektronix AWG 5208
        with IP address 192.168.20.43
        The arguments are required to follow the syntax.
        inst_name: 'Tektronix_AWG_5208'
        inst_visaAddress: 'TCPIP0::192.168.20.43::inst0::INSTR'
        timeout: 18000(sec)

        """
        self.instName = inst_name
        self.address = inst_visaAddress
        self.timeout = timeout
        self.rm = visa.ResourceManager()

    def connect(self):
        try:
            self.inst = self.rm.open_resource(self.address,
                                              read_termination='\n',
                                              write_termination=None)
            print(f'Connect to {self.instName} successfully\n' +
                  f'Statement: {self.inst.query("*IDN?")}')
        except visa.VisaIOError:
            print(f'Check "{self.instName}" has been plugin your PC')

    def disconnect(self):
        self.inst = self.rm.open_resource(self.address,
                                          read_termination='\n',
                                          write_termination=None)
        print(f'{self.instName} has been disconnected by user.')
        self.inst.close()

    def resetToDefault(self):
        sleep(1)
        self.inst.write('*RST')
        sleep(1)

    @staticmethod
    def get_inst_address():
        rm_ = visa.ResourceManager()
        for index, inst_address in enumerate(rm_.list_resources()):
            if index == 0:
                print('We have found the following instruments.')
            if 'ASRL' in inst_address:
                continue
            else:
                inst = rm_.open_resource(inst_address)
                print(f'Inst_name: {inst.query("*IDN?")}\n' +
                      f'Inst_address:{inst_address}\n' +
                      f'------------------------------------\n')
                del inst
        del rm_
