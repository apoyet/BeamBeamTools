import numpy as np
import pandas as pd
from helpers import *

def dictOpticsFromMADX(B1_twiss,B2_twiss,B1_survey,B2_survey):
    """
    This functions transforms the 4 DFs obtained from MAD-X into a dotdict with autocompletetion. 
    The output structure would be MADX_DICT.BEAM.Survey (or Twiss)
    """
    B1opticsDic = dotdict({'Twiss':B1_twiss['opticsDF'],'Survey':B1_survey['opticsDF']})
    B2opticsDic = dotdict({'Twiss':B2_twiss['opticsDF'],'Survey':B2_survey['opticsDF']})
    return dotdict({'B1':B1opticsDic,'B2':B2opticsDic})
    
def preparingOpticsFromMADX(MADX_DICT):
    """
    This function makes all the required optics post process needed to compute BB related values. 
    The input is a dotdict containing the survey and the twiss from MAD-X for each beam. 
    The output has the same structure, but contains post-processed data. 
    
    NB: as the input is a dotdict, please prepare the optics data in such a structure using _dictOpticsFromMADX
    
    ===== EXAMPLE =====
    MADX_DICT = preparingOpticsFromMADX(dictOpticsFromMADX(B1_twiss,B2_twiss,B1_survey,B2_survey))
    """
    # Mirroring
    B1_mirrored=MADX_DICT.B1.Twiss.copy()
    B1_mirrored.index=B1_mirrored.index-MADX_DICT.B1.Twiss.index[-1]
    B1_mirrored['S']=B1_mirrored['S']-MADX_DICT.B1.Twiss.index[-1]

    B2_mirrored=MADX_DICT.B2.Twiss.copy()
    B2_mirrored.index=B2_mirrored.index-MADX_DICT.B2.Twiss.index[-1]
    B2_mirrored['S']=B2_mirrored['S']-MADX_DICT.B2.Twiss.index[-1]

    B1=pd.concat([B1_mirrored,MADX_DICT.B1.Twiss])
    B2=pd.concat([B2_mirrored,MADX_DICT.B2.Twiss])


    B1SurveyMirrored=MADX_DICT.B1.Survey.copy()
    B1SurveyMirrored.index=B1SurveyMirrored.index-MADX_DICT.B1.Survey.index[-1]
    B1SurveyMirrored['S']=B1SurveyMirrored['S']-MADX_DICT.B1.Survey.index[-1]

    B2SurveyMirrored=MADX_DICT.B2.Survey.copy()
    B2SurveyMirrored.index=B2SurveyMirrored.index-MADX_DICT.B2.Survey.index[-1]
    B2SurveyMirrored['S']=B2SurveyMirrored['S']-MADX_DICT.B2.Survey.index[-1]

    # B1/2 survey
    B1_survey=pd.concat([B1SurveyMirrored,MADX_DICT.B1.Survey])
    B2_survey=pd.concat([B2SurveyMirrored,MADX_DICT.B2.Survey])

    #######========== SURVEY ==========#######

    # Filtering B1 and B2 DFs, in order to fullfill two conditions:
    # - in the 8 Long straight sections they are a n x Delta from the IR, Delta~25 ns *c (B1 and B2 DFs must have the
    # same length but not the same s)
    # - in the arcs the mechanical distance of the two reference orbits in s^{B1}_i and s^{B2}_i is 19.4 mm.

    myFilter=((B1_survey['NAME'].str.contains('^MB\..*B1$')) | 
              (B1_survey['NAME'].str.contains('^E\.')) |
              (B1_survey['NAME'].str.contains('BBLR')) |
              (B1_survey['NAME'].str.contains('^S\.')))

    B1_survey_filter=B1_survey[myFilter].copy()

    myFilter=((B2_survey['NAME'].str.contains('^MB\..*B2$')) | 
              (B2_survey['NAME'].str.contains('^E\.')) |
              (B2_survey['NAME'].str.contains('BBLR')) |
              (B2_survey['NAME'].str.contains('^S\.')))

    B2_survey_filter=B2_survey[myFilter].copy()

    # DeltaX and Delta Z computation from survey, taking into account the angle Theta

    DeltaX=B2_survey_filter['X'].values-B1_survey_filter['X'].values
    DeltaY=B2_survey_filter['Z'].values-B1_survey_filter['Z'].values

    meanTheta=(B1_survey_filter['THETA'].values+B2_survey_filter['THETA'].values)/2.

    myDeltaX=np.cos(meanTheta)*DeltaX-np.sin(meanTheta)*DeltaY
    myDeltaZ=np.sin(meanTheta)*DeltaX+np.cos(meanTheta)*DeltaY

    B1_survey_filter['myDeltaZ']=myDeltaZ
    B1_survey_filter['myDeltaX']=myDeltaX

    DeltaX=-B2_survey_filter['X'].values+B1_survey_filter['X'].values
    DeltaY=-B2_survey_filter['Z'].values+B1_survey_filter['Z'].values

    meanTheta=(B1_survey_filter['THETA'].values+B2_survey_filter['THETA'].values)/2.

    myDeltaX=np.cos(meanTheta)*DeltaX-np.sin(meanTheta)*DeltaY
    myDeltaZ=np.sin(meanTheta)*DeltaX+np.cos(meanTheta)*DeltaY

    B2_survey_filter['myDeltaZ']=myDeltaZ
    B2_survey_filter['myDeltaX']=myDeltaX

    # Phase advance at the IPS B1

    muX_IP1L = B1[B1['NAME']=='IP1.L1']['MUX'].values[0]
    muY_IP1L = B1[B1['NAME']=='IP1.L1']['MUY'].values[0]

    muX_IP2 = B1[B1['NAME']=='IP2']['MUX'].values[0]
    muY_IP2 = B1[B1['NAME']=='IP2']['MUY'].values[0]

    muX_IP3 = B1[B1['NAME']=='IP3']['MUX'].values[0]
    muY_IP3 = B1[B1['NAME']=='IP3']['MUY'].values[0]

    muX_IP4 = B1[B1['NAME']=='IP4']['MUX'].values[0]
    muY_IP4 = B1[B1['NAME']=='IP4']['MUY'].values[0]

    muX_IP5 = B1[B1['NAME']=='IP5']['MUX'].values[0]
    muY_IP5 = B1[B1['NAME']=='IP5']['MUY'].values[0]

    muX_IP6 = B1[B1['NAME']=='IP6']['MUX'].values[0]
    muY_IP6 = B1[B1['NAME']=='IP6']['MUY'].values[0]

    muX_IP7 = B1[B1['NAME']=='IP7']['MUX'].values[0]
    muY_IP7 = B1[B1['NAME']=='IP7']['MUY'].values[0]

    muX_IP8 = B1[B1['NAME']=='IP8']['MUX'].values[0]
    muY_IP8 = B1[B1['NAME']=='IP8']['MUY'].values[0]



    #######========== TWISS ==========#######

    # Filtering B1 and B2 DFs, in order to fullfill two conditions:
    # - in the 8 Long straight sections they are a n x Delta from the IR, Delta~25 ns *c (B1 and B2 DFs must have the
    # same length but not the same s)
    # - in the arcs the mechanical distance of the two reference orbits in s^{B1}_i and s^{B2}_i is 19.4 mm.

    myFilter=((B1['NAME'].str.contains('^MB\..*B1$')) | 
              (B1['NAME'].str.contains('^E\.')) |
              (B1['NAME'].str.contains('BBLR')) |
              (B1['NAME'].str.contains('^S\.')))

    B1_twiss_filter=B1[myFilter].copy()

    B1_twiss_filter['Delta MUX'] = 0
    B1_twiss_filter['Delta MUY'] = 0

    B1_twiss_filter['Ideal MUX'] = 0
    B1_twiss_filter['Ideal MUY'] = 0

    for i in B1_twiss_filter.index:
        if 'IP1_L' in B1_twiss_filter.loc[i,'NAME']:
            B1_twiss_filter.loc[i,'Delta MUX'] = -(muX_IP1L-B1_twiss_filter.loc[i,'MUX'])
            B1_twiss_filter.loc[i,'Ideal MUX'] = -0.25
            B1_twiss_filter.loc[i,'Delta MUY'] = -(muY_IP1L-B1_twiss_filter.loc[i,'MUY'])
            B1_twiss_filter.loc[i,'Ideal MUY'] = -0.25
        if 'IP1_R' in B1_twiss_filter.loc[i,'NAME']:
            B1_twiss_filter.loc[i,'Delta MUX'] = B1_twiss_filter.loc[i,'MUX']
            B1_twiss_filter.loc[i,'Ideal MUX'] = 0.25
            B1_twiss_filter.loc[i,'Delta MUY'] = B1_twiss_filter.loc[i,'MUX']
            B1_twiss_filter.loc[i,'Ideal MUY'] = 0.25
        if 'IP5_L' in B1_twiss_filter.loc[i,'NAME']:
            B1_twiss_filter.loc[i,'Delta MUX'] = B1_twiss_filter.loc[i,'MUX'] - muX_IP5
            B1_twiss_filter.loc[i,'Ideal MUX'] = -0.25
            B1_twiss_filter.loc[i,'Delta MUY'] = B1_twiss_filter.loc[i,'MUY'] - muY_IP5
            B1_twiss_filter.loc[i,'Ideal MUY'] = -0.25
        if 'IP5_R' in B1_twiss_filter.loc[i,'NAME']:
            B1_twiss_filter.loc[i,'Delta MUX'] = B1_twiss_filter.loc[i,'MUX'] - muX_IP5
            B1_twiss_filter.loc[i,'Ideal MUX'] = 0.25
            B1_twiss_filter.loc[i,'Delta MUY'] = B1_twiss_filter.loc[i,'MUY'] - muY_IP5
            B1_twiss_filter.loc[i,'Ideal MUY'] = 0.25

    myFilter=((B2['NAME'].str.contains('^MB\..*B2$')) | 
              (B2['NAME'].str.contains('^E\.')) |
              (B2['NAME'].str.contains('BBLR')) |
              (B2['NAME'].str.contains('^S\.')))

    B2_twiss_filter=B2[myFilter].copy()

    B2_twiss_filter['Delta MUX'] = 0
    B2_twiss_filter['Delta MUY'] = 0

    B2_twiss_filter['Ideal MUX'] = 0
    B2_twiss_filter['Ideal MUY'] = 0

    # Phase advance at the IPS B2

    muX_IP1L = B2[B2['NAME']=='IP1.L1']['MUX'].values[0]
    muY_IP1L = B2[B2['NAME']=='IP1.L1']['MUY'].values[0]

    muX_IP2 = B2[B2['NAME']=='IP2']['MUX'].values[0]
    muY_IP2 = B2[B2['NAME']=='IP2']['MUY'].values[0]

    muX_IP3 = B2[B2['NAME']=='IP3']['MUX'].values[0]
    muY_IP3 = B2[B2['NAME']=='IP3']['MUY'].values[0]

    muX_IP4 = B2[B2['NAME']=='IP4']['MUX'].values[0]
    muY_IP4 = B2[B2['NAME']=='IP4']['MUY'].values[0]

    muX_IP5 = B2[B2['NAME']=='IP5']['MUX'].values[0]
    muY_IP5 = B2[B2['NAME']=='IP5']['MUY'].values[0]

    muX_IP6 = B2[B2['NAME']=='IP6']['MUX'].values[0]
    muY_IP6 = B2[B2['NAME']=='IP6']['MUY'].values[0]

    muX_IP7 = B2[B2['NAME']=='IP7']['MUX'].values[0]
    muY_IP7 = B2[B2['NAME']=='IP7']['MUY'].values[0]

    muX_IP8 = B2[B2['NAME']=='IP8']['MUX'].values[0]
    muY_IP8 = B2[B2['NAME']=='IP8']['MUY'].values[0]

    for i in B2_twiss_filter.index:
        if 'IP1_L' in B2_twiss_filter.loc[i,'NAME']:
            B2_twiss_filter.loc[i,'Delta MUX'] = -(muX_IP1L-B1_twiss_filter.loc[i,'MUX'])
            B2_twiss_filter.loc[i,'Ideal MUX'] = -0.25
            B2_twiss_filter.loc[i,'Delta MUY'] = -(muY_IP1L-B1_twiss_filter.loc[i,'MUY'])
            B2_twiss_filter.loc[i,'Ideal MUY'] = -0.25
        if 'IP1_R' in B2_twiss_filter.loc[i,'NAME']:
            B2_twiss_filter.loc[i,'Delta MUX'] = B1_twiss_filter.loc[i,'MUX']
            B2_twiss_filter.loc[i,'Ideal MUX'] = 0.25
            B2_twiss_filter.loc[i,'Delta MUY'] = B1_twiss_filter.loc[i,'MUX']
            B2_twiss_filter.loc[i,'Ideal MUY'] = 0.25
        if 'IP5_L' in B2_twiss_filter.loc[i,'NAME']:
            B2_twiss_filter.loc[i,'Delta MUX'] = B2_twiss_filter.loc[i,'MUX'] - muX_IP5
            B2_twiss_filter.loc[i,'Ideal MUX'] = -0.25
            B2_twiss_filter.loc[i,'Delta MUY'] = B2_twiss_filter.loc[i,'MUY'] - muY_IP5
            B2_twiss_filter.loc[i,'Ideal MUY'] = -0.25
        if 'IP5_R' in B2_twiss_filter.loc[i,'NAME']:
            B2_twiss_filter.loc[i,'Delta MUX'] = B2_twiss_filter.loc[i,'MUX'] - muX_IP5
            B2_twiss_filter.loc[i,'Ideal MUX'] = 0.25
            B2_twiss_filter.loc[i,'Delta MUY'] = B2_twiss_filter.loc[i,'MUY'] - muY_IP5
            B2_twiss_filter.loc[i,'Ideal MUY'] = 0.25


    B1_twiss_filter['myDeltaX']=B2_twiss_filter['X'].values-B1_twiss_filter['X'].values
    B1_twiss_filter['myDeltaZ']=B2_twiss_filter['Y'].values-B1_twiss_filter['Y'].values

    B2_twiss_filter['myDeltaX']=B1_twiss_filter['X'].values-B2_twiss_filter['X'].values
    B2_twiss_filter['myDeltaZ']=B1_twiss_filter['Y'].values-B2_twiss_filter['Y'].values



    B1_twiss_filter['B2-B1 complex distance']= (B1_twiss_filter['myDeltaX']+B1_survey_filter['myDeltaX']) \
                                            + 1j*(B1_twiss_filter['myDeltaZ']+B1_survey_filter['myDeltaZ'])

    B2_twiss_filter['B1-B2 complex distance']= (B2_twiss_filter['myDeltaX']+B2_survey_filter['myDeltaX']) \
                                            + 1j*(B2_twiss_filter['myDeltaZ']+B2_survey_filter['myDeltaZ'])


    B1opticsDic = dotdict({'Twiss':B1_twiss_filter,'Survey':B1_survey_filter})
    B2opticsDic = dotdict({'Twiss':B2_twiss_filter,'Survey':B1_survey_filter})

    return dotdict({'B1':B1opticsDic,'B2':B2opticsDic})


def filterOpticsDF(BBES,beam,exp,bunch, B1Optics_BB,B2Optics_BB,removeHO=True):
    '''
    This function aims to filter the optics wrt to the previsouly prepared BBES structure. 
    Please set "removeHO" to False in case you want to conserve the HO in the optics. 
    '''
    # Copy

    B1Optics=B1Optics_BB[np.in1d(B1Optics_BB.index,BBES[beam][bunch][exp]['B1_RDV_position'])].copy()
    B2Optics=B2Optics_BB[np.in1d(B2Optics_BB.index,BBES[beam][bunch][exp]['B2_RDV_position'])].copy()

    # Partners

    B1Optics['partners']=BBES[beam][bunch][exp]['partners']
    B2Optics['partners']=BBES[beam][bunch][exp]['partners']
    
    if removeHO == True:
        # Removing the HO

        myIP = 'IP'+exp[2]
        myHO = 'BBLR_'+myIP+'_HO'+'.'+'B1'
        B1Optics = B1Optics[B1Optics.NAME != myHO]
        myHO = 'BBLR_'+myIP+'_HO'+'.'+'B2'
        B2Optics = B2Optics[B2Optics.NAME != myHO]

    return dotdict({'B1Optics':B1Optics,'B2Optics':B2Optics})

