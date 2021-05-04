import numpy as np
import matplotlib.pyplot as plt




### Building Pulse
class Waveform(object):
   
    def __init__(self):
        """
        Intitialize a Waveform object:
        The data structure of the waveform is 
        Dict { index : Tuple(Waveform, PropertyList[null/Pulse,pulsewidth
        ,flatLen,sigmaLen])}

        """
        self._WaveForm = dict()
        self._WaveFormList = list()
        #self._PulseFormList = list()
        #self._NullFormList  = list()

    ###Create Building blocks of the waveform 
     
    def GaussianPulse(self,sigmaLen, flatLen, Nsigma = 3):
        pulsewidth = flatLen + 2*Nsigma*sigmaLen + 1
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
        PropertyList = ["Gaussian",pulsewidth,flatLen,sigmaLen]
        GaussWfm = list(GaussWfm)
        GaussTuple   = (GaussWfm,PropertyList)

        return GaussTuple


    def SquarePulse(self,flatLen):
        
        #SquareWfm = np.ones(flatLen)
        SquareWfm    = [1]*flatLen
        SquarePulsewidth = flatLen
        SquaresigmaLen = 0
        PropertyList = ["Square",SquarePulsewidth,flatLen,SquaresigmaLen]
        SquareTuple  = (SquareWfm,PropertyList)

        return SquareTuple


    def NullPulse(self,nullLen):

        #NullWfm = np.zeros(nullLen,dtype = np.float64)
        NullWfm = [0]*nullLen
        NullPulsewidth = nullLen
        NullsigmaLen = 0
        PropertyList = ["Null",NullPulsewidth,nullLen,NullsigmaLen]
        NullTuple = (NullWfm,PropertyList)

        return NullTuple


    ### Edit Waveform

    def EncapsulateWfm(self,waveformTuple):

        self._WaveForm[len(self._WaveForm)] = waveformTuple 

        print(self._WaveForm)


    def SwapWaveForm(self,N_1,N_2):

        self._WaveForm[N_1-1], self._WaveForm[N_2-1] = self._WaveForm[N_2-1], self._WaveForm[N_1-1]

        print(self._WaveForm)


    def InverseWaveform(self):

        #for index in range(len(self._WaveForm.keys())):

        self._WaveForm = dict(reversed(list(self._WaveForm.items())))

        print(self._WaveForm)

    def RemoveWaveForm(self,Ndel):

        self._WaveForm.pop(Ndel-1)

        print(self._WaveForm)


    def ReplaceWaveForm(self,Nreplace,waveformTuple):

        self._WaveForm[Nreplace-1] = waveformTuple


    ### Get Waveform Info

    def GetWaveForm(self):
        WaveformList = list()
        for index in self._WaveForm.keys():
            WaveformList.append(self._WaveForm[index][0])
        WaveformList = sum(WaveformList, []) 
        #print(WaveformList)
        self._WaveFormList = WaveformList
        print(self._WaveFormList)
        #return self._WaveFormList
    

    def GetWaveFormInfo(self,Nwave = None):
        
        if(Nwave==None):
            print(self._WaveForm)
        else:
            print(self._WaveForm[Nwave-1][1])

    
    def GetWaveOffset(self,Nwave):

        WaveOffset = 0
        for index in range(Nwave-1):
            WaveOffset += self._WaveForm[index][1][1]

        print("The Offset of the " + str(Nwave) + " waveform: " + str(WaveOffset))
   


    
    def GetGaussSigmaLen(self,Nwave):
        #if ( == "Gaussian"):  
        pass
    def GetWavePulseWidth(self,Nwave):
        pass
        

if __name__ == '__main__':
    #test zone

    Arbit_Wfm = Waveform()
    a = Arbit_Wfm.SquarePulse(10)
    print(a)
    b = Arbit_Wfm.NullPulse(10)
    print(b)
    Arbit_Wfm.EncapsulateWfm(a)
    #print(wfm)
    Arbit_Wfm.EncapsulateWfm(b)
    #print(wfm2)
    Arbit_Wfm.GetWaveForm()
    Arbit_Wfm.SwapWaveForm(1,2)
    Arbit_Wfm.GetWaveForm()
    #Arbit_Wfm.InverseWaveform()
    #Arbit_Wfm.GetWaveForm()
    Arbit_Wfm.RemoveWaveForm(2)
    Arbit_Wfm.GetWaveForm()
    c = Arbit_Wfm.GaussianPulse(10,20)
    Arbit_Wfm.EncapsulateWfm(c)
    Arbit_Wfm.GetWaveForm()
    Arbit_Wfm.ReplaceWaveForm(2,a)
    Arbit_Wfm.GetWaveForm()
    Arbit_Wfm.GetWaveOffset(2)
    Arbit_Wfm.GetWaveFormInfo(2)
    Arbit_Wfm.GetWaveForm()
    Arbit_Wfm.GetWaveFormInfo()


    # Draft Code 
    #def GetWaveForm(self):
    #    for index in self._WaveForm.keys():
    #        self._WaveFormList.append(self._WaveForm[index])
    #    self._WaveFormList = sum(self._WaveFormList, []) 
    #    print(self._WaveFormList)
    #    #return self._WaveFormList

    #def Append_Waveform(self, Waveform_1, Waveform_2, default = True):
    #    
    #    #The Default case : waveform_2 is added at the end of the waveform_1 
    #    if (default == 1):
    #        Waveform_New = Waveform_1 + Waveform_2
    #    
    #    elif(default == 0):
    #        Waveform_New = Waveform_2 + Waveform_1
    #
    #    # Need to raise an error
    #    #else:
    # 
    #    return Waveform_New

    #def Inverse_Waveform(self, Waveform):
    #    
    #    
    #    #Waveform.reverse()
    #
    #    return Waveform[::-1]
    #    #return Waveform.reverse()
