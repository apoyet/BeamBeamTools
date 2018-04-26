class utilityFunctions:
    '''
    This class contains several usuful functions. 
    '''
    @staticmethod
    def setArrowLabel( ax, label='myLabel',arrowPosition=(0,0),labelPosition=(0,0), myColor='k', arrowArc_rad=-0.2):
        '''
        Credits to G. Sterbini.
        '''
        return ax.annotate(label,
                      xy=arrowPosition, xycoords='data',
                      xytext=labelPosition, textcoords='data',
                      size=10, color=myColor,va="center", ha="center",
                      bbox=dict(boxstyle="round4", fc="w",color=myColor,lw=2),
                      arrowprops=dict(arrowstyle="-|>",
                                      connectionstyle="arc3,rad="+str(arrowArc_rad),
                                      fc="w", color=myColor,lw=2), 
                      )
