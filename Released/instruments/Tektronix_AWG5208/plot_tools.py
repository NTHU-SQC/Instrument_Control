import matplotlib.pyplot as plt
# 20210405 Mon
# TODO(CCvitaminHsieh): Need to add "Mistake-proofing" if the user type 
#                       the unexpected arguments
#                       (e.g. the value is out of range)in function,
#                       it will remind the user that it raises some errors,
#                       which arguments are in wrong or unexpected situation.

def plt_wfmData_with_mkrData(result:dict):
    """
    Description:
        plot the waveform included wfmData and mkrData
    Args:
        result: a specified dict included 
                'mkrData', 'mkr_tone', 'wfmData', 'wfm_name'
    Example:
        if result is the following syntax, you can use the function
        to plot the wfmData with mkrData.

        result = {'mkrData': array([0., 0., 0., ..., 0., 0., 0.]),
                 'mkr_tone': 'mkr1',
                 'wfmData': array([0., 0., 0., ..., 0., 0., 0.]),
                 'wfm_name': 'gaussian_GaussFlat_1000pnts'}

        plt_wfmData_with_mkrData(result)
    """
    x = [i for i in range(len(result['wfmData']))]
    plt.plot(x, result['wfmData'], label='wfmData')
    plt.plot(x, result['mkrData'], 'r', label='mkrData')
    plt.legend()
    plt.xlabel('pts')
    plt.ylabel('Amplitude of AWG')
    plt.title(result['wfm_name'])
    plt.show()

def plt_qb_rd(seq_name:str, step_select:int, store_time_domain_seq:dict):
    """
    Descrition:
        La-la-la-la-la
        Ri-ras-ra-ra-ti-ti-ti-tas
        Ri-ri-ras, ri-ras-ra-ra-ti-ti-ti-ta
        Ra-ri-ras-ra-ra-ti-ti-ti-tas-ti-ri
        Rastis! Rastis! Ra-ti-ti-la! 
    Args:
        La-la-la-la-la
        Ri-ras-ra-ra-ti-ti-ti-tas
        Ri-ri-ras, ri-ras-ra-ra-ti-ti-ti-ta
        Ra-ri-ras-ra-ra-ti-ti-ti-tas-ti-ri
        Rastis! Rastis! Ra-ti-ti-la! 
    Example:
        La-la-la-la-la
        Ri-ras-ra-ra-ti-ti-ti-tas
        Ri-ri-ras, ri-ras-ra-ra-ti-ti-ti-ta
        Ra-ri-ras-ra-ra-ti-ti-ti-tas-ti-ri
        Rastis! Rastis! Ra-ti-ti-la! 
    """
    try:
        specified_step_qb_wfmData = store_time_domain_seq['QubitDrive'][step_select]['wfmData']
        specified_step_qb_mkrData = store_time_domain_seq['QubitDrive'][step_select]['mkrData']
        specified_step_rd_wfmData = store_time_domain_seq['ReadOut'][step_select]['wfmData']
        specified_step_rd_mkrData = store_time_domain_seq['ReadOut'][step_select]['mkrData']

        x = [i for i in range(len(specified_step_qb_wfmData))]

        plt.plot(x, specified_step_qb_wfmData,label='qb_wfmData')
        plt.plot(x, specified_step_qb_mkrData, 'y', label='qb_mkrData')
        plt.plot(x, specified_step_rd_wfmData, 'g',label='rd_wfmData')
        plt.plot(x, specified_step_rd_mkrData, 'r', label='rd_mkrData')
        
        plt.xlabel('pts')
        plt.ylabel('Amplitude of AWG')
        plt.title(seq_name + '_plot_step_select_' + str(step_select))
        plt.legend()
        # plt.figure(figsize=(60,40))
        plt.subplots_adjust(right=2)

        plt.show()
        
    except Exception :
        num_step = list(store_time_domain_seq['QubitDrive'].keys())
        print(f'Num Track Select Error: Out of the step select from {num_step[0]} to {num_step[-1]}')