import ROOT as r
from numpy import *
def setBinsToAr1D(hist,ar):#,xlow,xup):
    for i in range(len(ar)):
        hist.SetBinContent(i+1,ar[i])
def makeTH1fFromAr1D(ar,name='array',title='title',xlow=0,xup=None):
    # TH1(const char* name, const char* title, Int_t nbinsx, Double_t xlow, Double_t xup)
    nbinsx=len(ar)
    if not xup:
        xup=nbinsx

    tHist=r.TH1F(name,title,nbinsx,xlow,xup)
    setBinsToAr1D(tHist,ar)
    return tHist

def rwBuf2Array(buf,bufLen):
    al=[buf[idx] for idx in range(bufLen)]
    return array(al)


def fitGausPeaks(th,peaks):
    # th:    a thist which we've done some peak fitting to, and we want to get gaussian fits to those peaks
    # peaks: an np array of the x coords of the peaks we want to fit.
    # returns a list of tuples (const,mean,sigma), one entry for each peak in peaks

    peaks.sort()
    
    dxP=diff(peaks)
    # peaks: [ 231.5,  245.5,  260.5,  274.5,  288.5]
    # dxP:         [ 14.,    15.,    14.,    14.]
    fits=[]
    for idx in range(len(peaks)):
        if idx==0:
            dm=dxP[idx]/2.
        else:
            dm=dxP[idx-1]/2.
        if idx==len(peaks)-1:
            dp=dxP[idx-1]/2.
        else:
            dp=dxP[idx]/2.

        gf=th.Fit('gaus','QS','goff',peaks[idx]-dm,peaks[idx]+dp)
        fits.append((gf.Value(0),gf.Value(1),gf.Value(2)))
    return fits


 # EXT PARAMETER                                   STEP         FIRST   
 #  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
 #   1  Constant     8.59870e+01   6.10376e+00   1.45273e-02  -4.15609e-05
 #   2  Mean         2.59977e+02   1.20712e-01   4.91596e-04   1.20419e-04
 #   3  Sigma        2.81622e+00   1.74553e-01   4.66133e-05  -4.52088e-03


        # In [78]: gf.Value(0)
        # Out[78]: 479.3979941558617

        # In [79]: gf.Value(1)
        # Out[79]: 231.6665489234626

        # In [80]: gf.Value(2)
        # Out[80]: 1.606575935147517