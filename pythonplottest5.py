import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes


plt.rcParams.update({'font.size': 40, 'legend.fontsize': 30,'font.color': '#77933C', 'xtick.major.pad':25,          'legend.linewidth': 2})

bpT1R = []
bpT1G=[]
ubhT1R = []
ubhT1G=[]
bhT1R = []
bhT1G=[]


bpT2R = []
bpT2G=[]
ubhT2R = []
ubhT2G=[]
bhT2R = []
bhT2G=[]




bpT3R = []
bpT3G=[]
ubhT3R = []
ubhT3G=[]
bhT3R = []
bhT3G=[]

ubpT1R = []
ubpT1G=[]
ubpT2R = []
ubpT2G=[]
ubpT3R = []
ubpT3G=[]




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


with open('ravelresultsall16.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT1R.append( float(parts[0]))
        ubhT1R.append( float(parts[1]))
        bpT1R.append( float(parts[2]))
        ubpT1R.append( float(parts[3]))


with open('Postergavelresults16all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT1G.append( float(parts[2]))
        ubhT1G.append( float(parts[3]))
        bpT1G.append( float(parts[3]))
        ubpT1G.append( float(parts[3]))

with open('ravelresultsall32.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT2R.append( float(parts[0]))
        ubhT2R.append( float(parts[1]))
        bpT2R.append( float(parts[2]))
        ubpT2R.append( float(parts[3]))


with open('Postergavelresults32all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT2G.append( float(parts[2]))
        ubhT2G.append( float(parts[3]))
        bpT2G.append( float(parts[3]))        
        ubpT2G.append( float(parts[3]))


with open('ravelresultsall64.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT3R.append( float(parts[0]))
        ubhT3R.append( float(parts[1]))
        bpT3R.append( float(parts[2]))
        ubpT3R.append( float(parts[3]))


with open('Postergavelresults64all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bhT3G.append( float(parts[2]))
        ubhT3G.append( float(parts[3]))
        bpT3G.append( float(parts[3]))
        ubpT3G.append( float(parts[3]))
    





bhT1G = np.array(bhT1G)
ubhT1G = np.array(ubhT1G)
bpT1G = np.array(bpT1G)
ubpT1G = np.array(ubpT1G)
filteredbhT1G = bhT1G[~is_outlier(bhT1G)]
filteredubhT1G = ubhT1G[~is_outlier(ubhT1G)]
filteredbpT1G = bpT1G[~is_outlier(bpT1G)]
filteredubpT1G = ubpT1G[~is_outlier(ubpT1G)]


bhT2G = np.array(bhT2G)
ubhT2G = np.array(ubhT2G)
bpT2G = np.array(bpT2G)
ubpT2G = np.array(ubpT2G)
filteredbhT2G = bhT2G[~is_outlier(bhT2G)]
filteredubhT2G = ubhT2G[~is_outlier(ubhT2G)]
filteredbpT2G = bpT2G[~is_outlier(bpT2G)]
filteredubpT2G = ubpT2G[~is_outlier(ubpT2G)]


bhT3G = np.array(bhT3G)
ubhT3G = np.array(ubhT3G)
bpT3G = np.array(bpT3G)
ubpT3G = np.array(ubpT3G)
filteredbhT3G = bhT3G[~is_outlier(bhT3G)]
filteredubhT3G = ubhT3G[~is_outlier(ubhT3G)]
filteredbpT3G = bpT3G[~is_outlier(bpT3G)]
filteredubpT3G = ubpT3G[~is_outlier(ubpT3G)]



bhT1R = np.array(bhT1R)
ubhT1R = np.array(ubhT1R)
bpT1R = np.array(bpT1R)
ubpT1R = np.array(ubpT1R)
filteredbhT1R = bhT1R[~is_outlier(bhT1R)]
filteredubhT1R = ubhT1R[~is_outlier(ubhT1R)]
filteredbpT1R = bpT1R[~is_outlier(bpT1R)]
filteredubpT1R = ubpT1R[~is_outlier(ubpT1R)]


bhT2R = np.array(bhT2R)
ubhT2R = np.array(ubhT2R)
bpT2R = np.array(bpT2R)
ubpT2R = np.array(ubpT2R)
filteredbhT2R = bhT2R[~is_outlier(bhT2R)]
filteredubhT2R = ubhT2R[~is_outlier(ubhT2R)]
filteredbpT2R = bpT2R[~is_outlier(bpT2R)]
filteredubpT2R = ubpT2R[~is_outlier(ubpT2R)]


bhT3R = np.array(bhT3R)
ubhT3R = np.array(ubhT3R)
bpT3R = np.array(bpT3R)
ubpT3R = np.array(ubpT3R)
filteredbhT3R = bhT3R[~is_outlier(bhT3R)]
filteredubhT3R = ubhT3R[~is_outlier(ubhT3R)]
filteredbpT3R = bpT3R[~is_outlier(bpT3R)]
filteredubpT3R = ubpT3R[~is_outlier(ubpT3R)]



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



fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))

bp = axes[0].boxplot(A, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[0].boxplot(B, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[0].boxplot(C, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[0].boxplot(D, positions = [10, 11], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[1].boxplot(bA, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[1].boxplot(bB, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[1].boxplot(bC, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[1].boxplot(bD, positions = [10, 11], widths = 0.6,patch_artist=True)
setBoxColors(bp)


bp = axes[2].boxplot(cA, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[2].boxplot(cB, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[2].boxplot(cC, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColors(bp)

bp = axes[2].boxplot(cD, positions = [10, 11], widths = 0.6,patch_artist=True)
setBoxColors(bp)




axes[0].set_title('k=16',color='#77933C')
axes[1].set_title('k=32',color='#77933C')
axes[2].set_title('k=64',color='#77933C')
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
    ax.set_xticklabels(['BH', 'UBH', 'BP','UBP'],color='#77933C')
    ax.tick_params(axis='y', colors='#77933C')

    
for tic in axes[1].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
    
for tic in axes[2].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
# set axes limits and labels


hB, = axes[2].plot([0,0],'g-',linewidth = 5.0)
hR, = axes[2].plot([0,0],'-',color='violet', linewidth = 5.0)
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
