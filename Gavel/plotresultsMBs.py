import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes


plt.rcParams.update({'font.size': 40, 'legend.fontsize': 30,'font.color': '#77933C', 'xtick.major.pad':25,          'legend.linewidth': 2})



g3 = []
g4=[]
g5=[]
g6=[]
g7=[]



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
    setp(bp['boxes'][0], color='green')
    setp(bp['caps'][0], color='green')
    setp(bp['caps'][1], color='green')
    setp(bp['whiskers'][0], color='green')
    setp(bp['whiskers'][1], color='green')
    setp(bp['fliers'][0], color='green')
    setp(bp['fliers'][1], color='green')
    setp(bp['medians'][0], color='green')

    setp(bp['boxes'][1], color='violet')
    setp(bp['caps'][2], color='violet')
    setp(bp['caps'][3], color='violet')
    setp(bp['whiskers'][2], color='violet')
    setp(bp['whiskers'][3], color='violet')
    setp(bp['fliers'][2], color='violet')
    setp(bp['fliers'][3], color='violet')
    setp(bp['medians'][1], color='violet')

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


with open('JournalGavel16SFC.txt') as inf:
    for line in inf:
        parts = line.split("    ") # split line into parts
        if parts[4] == 3:
            g3.append(float(parts[2]))
        if parts[4] == 4:
            g4.append(float(parts[2]))
        if parts[4] == 5:
            g5.append(float(parts[2]))
        if parts[4] == 6:
            g6.append(float(parts[2]))
        if parts[4] == 7:
            g7.append(float(parts[2]))
            
        
# with open('Postergavelresults16all.txt') as inf:
#     for line in inf:
#         parts = line.split("    ") # split line into parts
#         bhT1G.append( float(parts[2]))
#         ubhT1G.append( float(parts[3]))
#         bpT1G.append( float(parts[3]))
#         ubpT1G.append( float(parts[3]))
# 
# with open('ravelresultsall32.txt') as inf:
#     for line in inf:
#         parts = line.split("    ") # split line into parts
#         bhT2R.append( float(parts[0]))
#         ubhT2R.append( float(parts[1]))
#         bpT2R.append( float(parts[2]))
#         ubpT2R.append( float(parts[3]))
# 
# 
# with open('Postergavelresults32all.txt') as inf:
#     for line in inf:
#         parts = line.split("    ") # split line into parts
#         bhT2G.append( float(parts[2]))
#         ubhT2G.append( float(parts[3]))
#         bpT2G.append( float(parts[3]))        
#         ubpT2G.append( float(parts[3]))
# 
# 
# with open('ravelresultsall64.txt') as inf:
#     for line in inf:
#         parts = line.split("    ") # split line into parts
#         bhT3R.append( float(parts[0]))
#         ubhT3R.append( float(parts[1]))
#         bpT3R.append( float(parts[2]))
#         ubpT3R.append( float(parts[3]))
# 
# 
# with open('Postergavelresults64all.txt') as inf:
#     for line in inf:
#         parts = line.split("    ") # split line into parts
#         bhT3G.append( float(parts[2]))
#         ubhT3G.append( float(parts[3]))
#         bpT3G.append( float(parts[3]))
#         ubpT3G.append( float(parts[3]))
#     





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



A= [filteredbhT1G,filteredbhT1R]
B=[filteredubhT1G,filteredubhT1R]
C=[bpT1G,bpT1R]
D=[ubpT1G,ubpT1R]

bA= [filteredbhT2G,filteredbhT2R]
bB=[filteredubhT2G,filteredubhT2R]
bC=[bpT2G,filteredbpT2R]
bD=[ubpT2G,ubpT2R]

cA= [filteredbhT3G,filteredbhT3R]
cB=[filteredubhT3G,filteredubhT3R]
cC=[bpT3G,filteredbpT3R]
cD=[ubpT3G,ubpT3R]



fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 5))

bp = axes[0].boxplot(filteredg3, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[0].boxplot(filteredg4, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[0].boxplot(filteredg5, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[0].boxplot(filteredg6, positions = [10, 11], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[0].boxplot(filteredg7, positions = [13, 14], widths = 0.6,patch_artist=True)
setBoxColors(bp)





axes[0].set_title('k=16',color='#77933C')
# axes[1].set_title('k=32',color='#77933C')
# axes[2].set_title('k=64',color='#77933C')
#axes[1].set_yscale('log')
#axes[0].set_yscale('log')
#axes[1].get_yaxis().set_ticks([])
#axes[2].set_yscale('log')
axes[0].set_ylabel('Time (ms)',size = 50, color='#77933C')
#axes[1].set_xlabel('Routing Application',size = 30,weight="bold")
for ax in axes:
    ax.yaxis.grid(b=True, which='major', color='dimgray', linestyle='--',linewidth = 5.0)
    
    #ax.set_xticks([y+1 for y in range(len(alldata))])

    ax.set_ylim([0,1000])
    ax.set_xlim([0,9])
    ax.set_xticks([1.5, 4.5, 7.5])
    ax.set_xticklabels(['3', '4', '5','6','7'],color='#77933C')
    ax.tick_params(axis='y', colors='#77933C')

    
for tic in axes[1].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
    
for tic in axes[2].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
# set axes limits and labels


hB, = axes[0].plot([0,0],'g-',linewidth = 5.0)
hR, = axes[0].plot([0,0],'-',color='violet', linewidth = 5.0)
legend = legend((hB, hR),('Gavel', 'Ravel'),loc=(0.55, .01), labelspacing=0.1)
#plt.legend(loc=2,prop={'size':6})
hB.set_visible(False)
hR.set_visible(False)
ltext = plt.gca().get_legend().get_texts()
plt.setp(ltext[0], fontsize = 20, color = 'g')
plt.setp(ltext[1], fontsize = 20, color = 'violet')
plt.tight_layout()
plt.subplots_adjust(bottom=0.1)
#plt.grid(b=True, which='both', color='dimgray',linestyle='-')
plt.setp(legend.get_texts(), fontsize='30')
plt.show()
