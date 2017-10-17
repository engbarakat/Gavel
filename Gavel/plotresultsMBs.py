import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes


#plt.rcParams.update({'font.size': 40, 'legend.fontsize': 30,'font.color': '#77933C', 'xtick.major.pad':25, 'legend.linewidth': 2})



g3 = []
g4=[]
g5=[]
g6=[]
g7=[]

r3 = []
r4=[]
r5=[]
r6=[]
r7=[]

# bpT1R = []
# bpT1G=[]
# ubhT1R = []
# ubhT1G=[]
# bhT1R = []
# bhT1G=[]
# 
# 
# bpT2R = []
# bpT2G=[]
# ubhT2R = []
# ubhT2G=[]
# bhT2R = []
# bhT2G=[]
# 
# 
# 
# 
# bpT3R = []
# bpT3G=[]
# ubhT3R = []
# ubhT3G=[]
# bhT3R = []
# bhT3G=[]
# 
# ubpT1R = []
# ubpT1G=[]
# ubpT2R = []
# ubpT2G=[]
# ubpT3R = []
# ubpT3G=[]




def setBoxColors(bp):
    setp(bp['boxes'][0], color='red')
#     setp(bp['caps'][0], color='red')
#     setp(bp['caps'][0], color='red')
#     setp(bp['whiskers'][0], color='red')
#     setp(bp['whiskers'][0], color='red')
#     setp(bp['fliers'][0], color='red')
#     setp(bp['fliers'][0], color='red')
    setp(bp['medians'][0], color='red')

    setp(bp['boxes'][1], color='green')
#     setp(bp['caps'][1], color='green')
#     setp(bp['caps'][1], color='green')
#     setp(bp['whiskers'][1], color='green')
#     setp(bp['whiskers'][1], color='green')
#     setp(bp['fliers'][1], color='green')
#     setp(bp['fliers'][1], color='green')
    setp(bp['medians'][1], color='green')

def setBoxColorsspe(bp):
    setp(bp['boxes'][0], color='violet')
    setp(bp['caps'][0], color='violet')
    setp(bp['caps'][1], color='violet')
    setp(bp['whiskers'][0], color='violet')
    setp(bp['whiskers'][1], color='violet')
    setp(bp['fliers'][0], color='violet')
    setp(bp['fliers'][1], color='violet')
    setp(bp['medians'][0], color='violet')




def is_outlier(points, thresh=2.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


with open('JournalGavelGeant2012SFC.txt') as inf:
    for line in inf:
        parts = line.split("\t") # split line into parts
        #print parts[4].rstrip()
        if parts[4].rstrip() == '3':
            #print '3333333333333333333333333333333'
            g3.append(float(parts[2]))
        elif parts[4].rstrip() == '4':
            g4.append(float(parts[2]))
        elif parts[4].rstrip() == '5':
            g5.append(float(parts[2]))
        elif parts[4].rstrip() == '6':
            g6.append(float(parts[2]))
        elif parts[4].rstrip() == '7':
            g7.append(float(parts[2]))

with open('ravelGeant2012SFC.txt') as inf:
    for line in inf:
        parts = line.split('\t')
        r3.append(float(parts[0])*2)
        r4.append(float(parts[1])*2)
        r5.append(float(parts[2])*2)
        r6.append(float(parts[3])*2)
        r7.append(float(parts[4])*2)
        
     





g3 = np.array(g3)
filteredg3 = g3[~is_outlier(g3)]
g4 = np.array(g4)
filteredg4 = g4[~is_outlier(g4)]
g5 = np.array(g5)
filteredg5 = g5[~is_outlier(g5)]
g6 = np.array(g6)
filteredg6 = g6[~is_outlier(g6)]
g7 = np.array(g7)
filteredg7 = g7[~is_outlier(g7)]




r3 = np.array(r3)
filteredr3 = r3[~is_outlier(r3)]
r4 = np.array(r4)
filteredr4 = r4[~is_outlier(r4)]
r5 = np.array(r5)
filteredr5 = r5[~is_outlier(r5)]
r6 = np.array(r6)
filteredr6 = r6[~is_outlier(r6)]
r7 = np.array(r7)
filteredr7 = r7[~is_outlier(r7)]



A= [filteredr3,filteredg3]
B=[filteredr4,filteredg4]
C=[filteredr5,filteredg5]
D=[filteredr6,filteredg6]
E=[filteredr7,filteredg7]
# 
# bA= [filteredbhT2G,filteredbhT2R]
# bB=[filteredubhT2G,filteredubhT2R]
# bC=[bpT2G,filteredbpT2R]
# bD=[ubpT2G,ubpT2R]
# 
# cA= [filteredbhT3G,filteredbhT3R]
# cB=[filteredubhT3G,filteredubhT3R]
# cC=[bpT3G,filteredbpT3R]
# cD=[ubpT3G,ubpT3R]



#fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 5))
fig, axes = plt.subplots()
bp = axes.boxplot(A, positions = [1,2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes.boxplot(B, positions = [4,5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes.boxplot(C, positions = [7,8], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes.boxplot(D, positions = [10,11], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes.boxplot(E, positions = [13,14], widths = 0.6,patch_artist=True)
setBoxColors(bp)





#axes.set_title('Geant2012',color='Black',size=20)
# axes[1].set_title('k=32',color='#77933C')
# axes[2].set_title('k=Geant2012',color='#77933C')
axes.set_yscale('log')
#axes[0].set_yscale('log')
#axes[1].get_yaxis().set_ticks([])
#axes[2].set_yscale('log')
axes.set_ylabel('Time (ms)',size = 50, color='Black')
axes.set_xlabel('Functions\' Chain Size',size = 50, color='Black')

axes.yaxis.grid(b=True, which='major', color='dimgray', linestyle='--',linewidth = 5.0)
axes.set_ylim([1,8000])
axes.set_xlim([0,16])
axes.set_xticks([1.5, 4.5, 7.5,10.5,13.5])
axes.set_xticklabels(['3', '4', '5','6','7'],color='black',size=25)
axes.tick_params(axis='y', colors='black',size=25)
    
for tic in axes.yaxis.get_major_ticks():
    tic.label.set_fontsize(25)
    
#for tic in axes[2].yaxis.get_major_ticks():
#    tic.label1On = tic.label2On = False
# set axes limits and labels


hB, = axes.plot([0,0],'g-',linewidth = 3.0)
hR, = axes.plot([0,0],'-',color='Red', linewidth = 3.0)
legend = legend((hB, hR),('Gavel', 'Ravel'),loc=(0.8, .8), labelspacing=0.1)
#plt.legend(loc=2,prop={'size':6})
hB.set_visible(False)
hR.set_visible(False)
ltext = plt.gca().get_legend().get_texts()
plt.setp(ltext[0], fontsize = 20, color = 'g')
plt.setp(ltext[1], fontsize = 20, color = 'Red')
plt.tight_layout()
plt.subplots_adjust(bottom=0.1)
#plt.grid(b=True, which='both', color='dimgray',linestyle='-')
plt.setp(legend.get_texts(), fontsize='30')
plt.show()
