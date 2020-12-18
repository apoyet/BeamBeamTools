import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def _setArrowLabel(ax, label='myLabel',arrowPosition=(0,0),labelPosition=(0,0), myColor='k', arrowArc_rad=-0.2, textSize=10):
        return ax.annotate(label,
                      xy=arrowPosition, xycoords='data',
                      xytext=labelPosition, textcoords='data',
                      size=textSize, color=myColor,va="center", ha="center",
                      bbox=dict(boxstyle="round4", fc="w",color=myColor,lw=2),
                      arrowprops=dict(arrowstyle="-|>",
                                      connectionstyle="arc3,rad="+str(arrowArc_rad),
                                      fc="w", color=myColor,lw=2), 
                      )

def _setShadedRegion(ax,color='g' ,xLimit=[0,1], yLimit='FullRange',alpha=.1):
    """
    setShadedRegion(ax,color='g' ,xLimit=[0,1],alpha=.1)
    ax: plot axis to use
    color: color of the shaded region
    xLimit: vector with two scalars, the start and the end point
    alpha: transparency settings
    yLimit: if set to "FullRange" shaded the entire plot in the y direction
    If you want to specify an intervall, please enter a two scalar vector as xLimit
    """
    if yLimit=='FullRange':
        aux=ax.get_ylim()
        plt.gca().fill_between(xLimit, [aux[0],aux[0]],  [aux[1],aux[1]],color=color, alpha=alpha)
        ax.set_ylim(aux)
    else:
        plt.gca().fill_between(xLimit, 
                    [yLimit[0],yLimit[0]],  [yLimit[1],yLimit[1]],color=color, alpha=alpha)

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
        _setArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=0.2)
        _setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=0.2)
    else:
        _etArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=-0.2)
        _setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=-0.2)
    plt.grid(ls=':')
    return ax1


def plot_BBMatrix(BBMatrixLHC, B1_bunches, B2_bunches,alpha=.2, width=1):
        """
        It plots a beam-beam matrix.

        Example:
        myMatrix=computeBBMatrix(numberOfLRToConsider=20)
        fillingSchemeDF=myToolbox.cals2pnd(MD1Toolbox.getFillingPattern(),
                                   datetime.datetime(2017,9,13,18),
                                   datetime.datetime(2017,9,13,18,1))
        B1_bunches=np.where(fillingSchemeDF.iloc[0]['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'])[0]
        B2_bunches=np.where(fillingSchemeDF.iloc[0]['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'])[0]

        myToolbox.plot_BBMatrix(BBMatrixLHC, B1_bunches, B2_bunches)
        """ 
        plt.figure(figsize=(10,10))
        plt.jet()
        plt.imshow(BBMatrixLHC,interpolation='none')
        plt.axis('tight')
        plt.xlabel('BEAM 2')
        plt.ylabel('BEAM 1')
        plt.axis('equal')
        plt.axis('tight');
        plt.tick_params(direction='inout')
        for i in B1_bunches:
            _setShadedRegion(plt.gca(), xLimit=[i-width+1, i+width],alpha=alpha,color='w')

        for i in B2_bunches:
            plt.gca().fill_between([0,3564], [i-width+1,i-width+1],  [i+width,i+width],color='w', alpha=alpha)

        _setArrowLabel(ax=plt.gca(),label='IP1/5',labelPosition=(2000,2000), arrowPosition=(2000,2000), myColor='k')
        _setArrowLabel(ax=plt.gca(),label='IP2',labelPosition=(2000,1100), arrowPosition=(2000,1100), myColor='k')
        _setArrowLabel(ax=plt.gca(),label='IP8',labelPosition=(2000,2900), arrowPosition=(2000,2900), myColor='k')
        _setArrowLabel(ax=plt.gca(),label='IP8',labelPosition=(3130,3564-3130), arrowPosition=(3130,3564-3130), myColor='k')
        _setArrowLabel(ax=plt.gca(),label='IP2',labelPosition=(3564-3130,3130), arrowPosition=(3564-3130,3130), myColor='k')
        return plt.gca()
