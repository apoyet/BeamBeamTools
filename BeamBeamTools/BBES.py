import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from helpers import *


def _bunch_BB_pattern(Bunch,BBMatrixLHC):
    '''
    It returns the beam-beam pattern of a bunch of B1 and B2 [adimensional array of integer] in ALICE, ATLAS, CMS, LHCB.
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


def _beam_BB_pattern(BBMatrixLHC,B1_fillingScheme=np.array([0,1,2,3]),B2_fillingScheme=np.array([0,1,2,3])):
    """
    It returns a dictionary structure with the BB encounters of B1 and B2 taking into account the filling schemes.
    - BBMatrixLHC [adimensional integer array]: the LHC BB matrix
    - B1_fillingScheme [adimensional integer array]: the B1 filling scheme.
    - B2_fillingScheme [adimensional integer array]: the B2 filling scheme.
    The dictionary structure has the following hierarchy:
    - BEAM >> BUNCH >> EXPERIMENT >> PARTNERS
    - BEAM >> BUNCH >> EXPERIMENT >> RDV_INDEX
    All the positions are referred to the positive direction of B1 (clockwise in LHC).
    WARNING: the bunch number is defined wrt the negative direction of each beam.
    """
    experiments=['IR1','IR2','IR5','IR8']
    #B1
    B1_BB_pattern=dotdict({})
    for i in B1_fillingScheme:
        bunch_aux=dotdict({})
        results=bunch_BB_pattern(Bunch=i,BBMatrixLHC=BBMatrixLHC)
        for j in experiments:
            bunch_exp=dotdict({})
            B1=results['B2'][j]
            aux = np.intersect1d(B1,B2_fillingScheme)
            myPosition = -((np.where(np.in1d(B1,aux))[0])-(len(B1)-1)/2)
            bunch_exp.update({'partners' : aux,'RDV_index':myPosition[-1::-1]})
            bunch_aux.update({str(j): bunch_exp})
        B1_BB_pattern.update({'b'+str(i):bunch_aux})
    #B2
    B2_BB_pattern=dotdict({})
    for i in B2_fillingScheme:
        bunch_aux=dotdict({})
        results=bunch_BB_pattern(Bunch=i,BBMatrixLHC=BBMatrixLHC)
        for j in experiments:
            bunch_exp=dotdict({})
            B2=results['B2'][j] # Full machine --> TODO: write it in a more symmetric way...
            aux = np.intersect1d(B2,B1_fillingScheme)
            myPosition = ((np.where(np.in1d(B2,aux))[0])-(len(B2)-1)/2)
            bunch_exp.update({'partners' : aux,'RDV_index':myPosition[-1::-1]})
            bunch_aux.update({str(j): bunch_exp})
        B2_BB_pattern.update({'b'+str(i):bunch_aux})

    beam_BB_pattern={'B1':B1_BB_pattern,'B2':B2_BB_pattern}
    return dotdict(beam_BB_pattern)


def plotBunchBBPattern(beam_BB_pattern,beam='B1',exp='IR1',bunch='b400'):
    """
    It returns a plot of the beam BB pattern.
    - beam_BB_pattern [dotdict]: contains the beam BB pattern
    """
    x=beam_BB_pattern[beam][bunch][exp]['RDV_index']
    y=[1]*len(x)
    plt.plot(x,y,'ok')
    encounters=beam_BB_pattern[beam][bunch][exp]['partners']

    plt.xlim(-25,25)
    plt.ylim(.94, 1.06)

    plt.yticks([])
    plt.xlabel('BBLR encounter position')
    ax1=plt.gca()
    plt.title(beam+ ', ' + exp + ', bunch=' + bunch)

    if beam=='B1':
        myToolbox.setArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=0.2)
        myToolbox.setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=0.2)
    else:
        myToolbox.setArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=-0.2)
        myToolbox.setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=-0.2)
    plt.grid(ls=':')
    return ax1

def optics_BB_pattern(BBMatrixLHC,B1_fillingScheme, B2_fillingScheme,B1Optics_BB,B2Optics_BB):
        """It returns the final BBES structure as a dot_dict, containing also the RDV position wrt B1 and B2 optics.
        - B1_fillingScheme [adimensional integer array]: the B1 filling scheme.
        - B2_fillingScheme [adimensional integer array]: the B2 filling scheme.
        - B1Optics_BB [pnd DF]: B1 optics.
        - B2Optics_BB [pnd DF]: B2 optics.
        The dictionary structure has the following hierarchy:
        - BEAM >> BUNCH >> EXPERIMENT >> PARTNERS
        - BEAM >> BUNCH >> EXPERIMENT >> RDV_INDEX
        - BEAM >> BUNCH >> EXPERIMENT >> B1_RDV_POSITION
        - BEAM >> BUNCH >> EXPERIMENT >> B2_RDV_POSITION
        """
        length = len(B1Optics_BB[B1Optics_BB['NAME'].str.contains('BBLR_IP1_R_')])
        opticsIndex = np.arange(-length/2,1+length/2) 
        results=_beam_BB_pattern(BBMatrixLHC,B1_fillingScheme, B2_fillingScheme)

        # ***ATLAS***

        aux1=B1Optics_BB[(B1Optics_BB['S']<260) & (B1Optics_BB['S']>-260)]
        aux1=aux1['S'].values

        aux2=B2Optics_BB[(B2Optics_BB['S']<260) & (B2Optics_BB['S']>-260)]
        aux2=aux2['S'].values

        #B1
        bunches = ['b'+str(e) for e in B1_fillingScheme]
        for i in bunches:
            exp = results['B1'][i]['IR1']
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        #B2
        bunches = ['b'+str(e) for e in B2_fillingScheme]
        for i in bunches:
            exp = results['B2'][i]['IR1']
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        # ***ALICE***

        aux1=B1Optics_BB[(B1Optics_BB['S']<3600) & (B1Optics_BB['S']>3070)]
        aux1=aux1['S'].values

        aux2=B2Optics_BB[(B2Optics_BB['S']<3600) & (B2Optics_BB['S']>3070)]
        aux2=aux2['S'].values

        #B1
        bunches = ['b'+str(e) for e in B1_fillingScheme]
        for i in bunches:
            exp = results['B1'][i]['IR2']
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        #B2
        bunches = ['b'+str(e) for e in B2_fillingScheme]
        for i in bunches:
            exp = results['B2'][i]['IR2']
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})


        # ***CMS***

        aux1=B1Optics_BB[(B1Optics_BB['S']<13590) & (B1Optics_BB['S']>13061)]
        aux1=aux1['S'].values

        aux2=B2Optics_BB[(B2Optics_BB['S']<13590) & (B2Optics_BB['S']>13061)]
        aux2=aux2['S'].values

        #B1
        bunches = ['b'+str(e) for e in B1_fillingScheme]
        for i in bunches:
            exp = results['B1'][i]['IR5']
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        #B2
        bunches = ['b'+str(e) for e in B2_fillingScheme]
        for i in bunches:
            exp = results['B2'][i]['IR5']
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        # ***LHCB***

        aux1=B1Optics_BB[(B1Optics_BB['S']<23580) & (B1Optics_BB['S']>23057.2)]
        aux1=aux1['S'].values

        aux2=B2Optics_BB[(B2Optics_BB['S']<23580) & (B2Optics_BB['S']>23057.2)]
        aux2=aux2['S'].values

        #B1
        bunches = ['b'+str(e) for e in B1_fillingScheme]
        for i in bunches:
            exp = results['B1'][i]['IR8']
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        #B2
        bunches = ['b'+str(e) for e in B2_fillingScheme]
        for i in bunches:
            exp = results['B2'][i]['IR8']
            exp.update({'B2_RDV_position': aux2[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})
            exp.update({'B1_RDV_position': aux1[np.where(np.in1d(opticsIndex,exp['RDV_index']))]})

        return results
    
    
  
def computeBBMatrix(numberOfLRToConsider=20):
        """
        It returns a beam-beam matrix. 
        To obtain the BB pattern of the bunch N of B1 you have to consider the N-row (e.g., BBMatrix[N,:]).
        
        The matrix will have a value 1,2,5,8 when there is a HO respectively in IP1,2,5,8.
        The matrix will have a value 10,20,50,80 when there is a LR respectively in IP1,2,5,8.
        
        It assumes that the positions of the IPs and the convention of the B1/B2 bunch numbering is such that.
        1. B1 Bunch 0 meets B2 Bunch 0 in IP1 and 5.
        2. B1 Bunch 0 meets B2 Bunch 891 in IP2.
        2. B1 Bunch 0 meets B2 Bunch 2670 in IP8.

        Example:
        myMatrix=computeBBMatrix(numberOfLRToConsider=20)
        """ 
        availableBunchSlot=3564
        BBMatrixLHC =np.zeros([availableBunchSlot,availableBunchSlot]);

        #numberOfLRToConsider=20;

        # HO in IP1 and IP5
        index=np.arange(availableBunchSlot)
        BBMatrixLHC[index,index]=1

        # BBLR in IP1 and IP5
        for i in range(1,numberOfLRToConsider+1):
            index=np.arange(availableBunchSlot-i)
            BBMatrixLHC[index,index+i]=10
            BBMatrixLHC[index,index-i]=10
            BBMatrixLHC[index+i,index]=10
            BBMatrixLHC[index-i,index]=10

        # HO in IP2
        IP2slot=availableBunchSlot/4
        index=np.arange(availableBunchSlot-IP2slot)
        BBMatrixLHC[index,index+IP2slot]=2
        index=np.arange(availableBunchSlot-IP2slot,availableBunchSlot)
        BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)]=2

        # BBLR in IP2
        for i in range(1,numberOfLRToConsider+1):
            index=np.arange(availableBunchSlot-IP2slot-i)
            BBMatrixLHC[index,index+IP2slot+i]=20
            BBMatrixLHC[index+i,index+IP2slot]=20
            BBMatrixLHC[index,index+IP2slot-i]=20
            BBMatrixLHC[index-i,index+IP2slot]=20
            index=np.arange(availableBunchSlot-IP2slot,availableBunchSlot-i)
            BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)+i]=20
            BBMatrixLHC[index+i,index-(availableBunchSlot-IP2slot)]=20
            BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)-i]=20
            BBMatrixLHC[index-i,index-(availableBunchSlot-IP2slot)]=20

        # HO in IP8
        IP8slot=availableBunchSlot/4*3-3
        index=np.arange(availableBunchSlot-IP8slot)
        BBMatrixLHC[index,index+IP8slot]=8
        index=np.arange(availableBunchSlot-IP8slot,availableBunchSlot)
        BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)]=8

        # BBLR in IP8
        for i in range(1,numberOfLRToConsider+1):
            index=np.arange(availableBunchSlot-IP8slot-i)
            BBMatrixLHC[index,index+IP8slot+i]=80
            BBMatrixLHC[index+i,index+IP8slot]=80
            BBMatrixLHC[index,index+IP8slot-i]=80
            BBMatrixLHC[index-i,index+IP8slot]=80
            index=np.arange(availableBunchSlot-IP8slot,availableBunchSlot-i)
            BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)+i]=80
            BBMatrixLHC[index+i,index-(availableBunchSlot-IP8slot)]=80
            BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)-i]=80
            BBMatrixLHC[index-i,index-(availableBunchSlot-IP8slot)]=80

        return BBMatrixLHC;
    
   
