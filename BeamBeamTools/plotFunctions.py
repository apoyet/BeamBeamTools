import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def _setArrowLabel(ax, label='myLabel',arrowPosition=(0,0),labelPosition=(0,0), myColor='k', arrowArc_rad=-0.2):
        return ax.annotate(label,
                      xy=arrowPosition, xycoords='data',
                      xytext=labelPosition, textcoords='data',
                      size=10, color=myColor,va="center", ha="center",
                      bbox=dict(boxstyle="round4", fc="w",color=myColor,lw=2),
                      arrowprops=dict(arrowstyle="-|>",
                                      connectionstyle="arc3,rad="+str(arrowArc_rad),
                                      fc="w", color=myColor,lw=2), 
                      )


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
