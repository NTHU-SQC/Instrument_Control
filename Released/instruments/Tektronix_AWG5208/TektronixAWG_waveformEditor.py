import numpy as np
import matplotlib.pyplot as plt
from instruments.Tektronix_AWG5208.funcs import gauss 

# class Waveform_Plot:
#     @staticmethod
#     def check_dependency():
#         try:
#             import matplotlib
#             print(f'Numpy version: {np.__version__}')
#             print(f'Matplotlib version: {matplotlib.__version__}')
#         except ModuleNotFoundError as reason:
#             print('Need to install the dependencies: ', reason)

#     def plotSingleGaussian(self, wfmData,
#                             auxiliaryMode=False, aux_start: int = 0, aux_end: int = 0) -> None:
#         xData = np.linspace(0, len(wfmData) - 1, len(wfmData))
#         yData = wfmData

#         if auxiliaryMode is True:
#             #xmarker = {'orginal':0, 'start_offset': aux_start, 'duration': aux_end, 'final':len(wfmData)}
#             xmarker = [0, aux_start, aux_end, len(wfmData)]
#             yScale = 1.35
#             # add a vertical line across the axes, and add arrow.
#             for index in range(len(xmarker)-1):
#                 plt.annotate('', xy=(xmarker[index], 1.25), xycoords='data',
#                              xytext=(xmarker[index+1], yScale-0.1), textcoords='data',
#                              arrowprops={'arrowstyle': '<->'})
#             for index in range(len(xmarker)):
#                 arrowcolor = 'red' if (index == 1) or (index == 2) else 'green'
#                 plt.axvline(xmarker[index], 0,
#                             linestyle='dotted', color=arrowcolor)
#             plt.ylim(0, yScale)

#         plt.plot(xData, yData)
#         plt.show()


class Waveform:
    # def __init__(self):
    #     """
    #     Intitialize a Waveform object:
    #     The data structure of the waveform is 
    #     Dict { index : Tuple(Waveform, PropertyList[null/Pulse,pulsewidth
    #     ,flatLen,sigmaLen])}

    #     """
    #     self._waveform_dict = dict()
    #     self._waveform_list = list()
    #     #self._PulseFormList = list()
    #     #self._NullFormList  = list()

    """
    Create Building blocks of the waveform 
    """
    def gauss_square_pulse(self, sigma:int, flat:int, num_sigma=3)->list:
        # parameters for making a gaussian
        stdev_width = num_sigma * sigma
        pulse_len = (2 * num_sigma * sigma) + flat 

        # initialize x-axis(wfm_data) and y-axis(tlist)
        wfm_data = np.zeros(pulse_len)
        tlist = [i for i in range(len(wfm_data))]

        # store the specified value to "wfm_data"
        for i in range(len(wfm_data)):
            # Rising
            if i <= stdev_width:
                wfm_data[i] = gauss(sigma, tlist[i], stdev_width)
            # Flatten
            elif (i > stdev_width) and (i < stdev_width+flat):
                wfm_data[i] = 1
            # Decay
            else:
                wfm_data[i] = gauss(sigma, tlist[i], flat+stdev_width)
        return wfm_data

    def waveform_shape(self, wfm_totlen:int, offset:int, wfm_data:list)->list:
        # defined a array with "0" elements
        # replace the "0" elements with gaussian square pulse
        start, end = offset, offset+len(wfm_data)
        wfm_init = np.zeros(wfm_totlen)
        wfm_init[start:end] = wfm_data
        return wfm_init

    def marker_shape(self, wfm_totlen:int, offset:int, mkr_duration:int)->list:
        # defined a array with "0" elements
        # replace the "0" elements with gaussian square pulse
        start, end = offset, offset+mkr_duration
        mkr_init = np.zeros(wfm_totlen)
        mkr_init[start:end] = np.ones(mkr_duration)
        return mkr_init

    def multipulse_insert(self, wfm_totlen:int, *pulse_offset:tuple, **pulse_array:dict)->list:
        """
        Example:
            high_step = np.ones(2)
            x = [i for i in range(10)]
            y = multipulse_merge(len(x), 1, 5, h1=high_step, h2=high_step)

            plt.scatter(x,y)
            plt.show()
        """
        i, wfm_init = 0, np.zeros(wfm_totlen)

        for shape in pulse_array.values():
            start, end = pulse_offset[i], pulse_offset[i]+len(shape)
            wfm_init[start:end] = list(shape)
            i += 1

        return wfm_init


if __name__ == '__main__':
    """
    Gaussian Demo
    """
    # pulse_test = Waveform()
    # wfmData = pulse_test.gauss_square_pulse(5, 50)
    # x = [i for i in range(len(wfmData))]
    # plt.plot(x, wfmData)
    # plt.show()
    """
    MultiPulse Insert
    """
    # demo_v1 = Waveform()
    # high_step = np.ones(150)
    # x = [i for i in range(1000)]
    # y = demo_v1.multipulse_insert(len(x), 100, 500, h1=high_step, h2=high_step)
    
    # plt.scatter(x,y)
    # plt.show()

    # demo_v2 = Waveform()
    # gaussian = demo_v2.gauss_square_pulse(50, 500)
    # offset = (1000, 5000)
    # gauss_box = {'h1':gaussian, 'h2':gaussian}
    # x = [i for i in range(10000)]
    # y = demo_v2.multipulse_insert(len(x), *offset, **gauss_box)
    
    # plt.scatter(x,y)
    # plt.show()
    pass