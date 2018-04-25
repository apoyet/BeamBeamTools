import pandas as pd 
import numpy as np


def bunch_BB_pattern(Bunch,BBMatrixLHC):
    '''It returns the beam-beam pattern of a bunch of B1 and B2 [adimensional array of integer] in ALICE, ATLAS, CMS, LHCB.
    - Bunch [adimensional integer]: the bunch number in B1 and B2 to consider.
    - BBMatrixLHC [adimensional integer matrix]: the beam-beam matrix to consider (see myToolbox.computeBBMatrix?).
    The returned array is ordered with respect to the positive direction of B1 (clockwise in LHC).
    WARNING: the bunch number is defined wrt the negative direction of each beam.
    '''
    BBVector=BBMatrixLHC[Bunch,:]
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==10)[0])/2
    HO_in_IP=BBVector==1
    LR_in_IP=BBVector==10
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux,  numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    B2=B1[::-1]
    resultsB1={'IR1':B1,
         'IR5':B1}
    resultsB2={'IR1':B2,
         'IR5':B2}
    HO_in_IP=BBVector==2
    LR_in_IP=BBVector==20
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    B2=B1[::-1]
    resultsB1.update({'IR2':B1})
    resultsB2.update({'IR2':B2})

    HO_in_IP=BBVector==8
    LR_in_IP=BBVector==80
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    B2=B1[::-1]
    resultsB1.update({'IR8':B1})
    resultsB2.update({'IR8':B2})
    results={'B1':resultsB1, 'B2':resultsB2}
    return results
