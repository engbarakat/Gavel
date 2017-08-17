import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes


plt.rcParams.update({'font.size': 22, 'font.weight':'bold'})

data64 = []
data264=[]
data32 = []
data232=[]
data16 = []
data216=[]





bdata64 = []
bdata264=[]
bdata32 = []
bdata232=[]
bdata16 = []
bdata216=[]




cdata64 = []
cdata264=[]
cdata32 = []
cdata232=[]
cdata16 = []
cdata216=[]






def setBoxColors(bp):
    setp(bp['boxes'][0], color='green')
    setp(bp['caps'][0], color='green')
    setp(bp['caps'][1], color='green')
    setp(bp['whiskers'][0], color='green')
    setp(bp['whiskers'][1], color='green')
    setp(bp['fliers'][0], color='green')
    setp(bp['fliers'][1], color='green')
    setp(bp['medians'][0], color='green')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    setp(bp['fliers'][2], color='red')
    setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

def setBoxColorsspe(bp):
    setp(bp['boxes'][0], color='red')
    setp(bp['caps'][0], color='red')
    setp(bp['caps'][1], color='red')
    setp(bp['whiskers'][0], color='red')
    setp(bp['whiskers'][1], color='red')
    setp(bp['fliers'][0], color='red')
    setp(bp['fliers'][1], color='red')
    setp(bp['medians'][0], color='red')



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
        data16.append( float(parts[0]))
        data32.append( float(parts[1]))
        data64.append( float(parts[2]))
        
        #data264.append( float(parts[3]))


with open('Postergavelresults16all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        data216.append( float(parts[2]))
        data232.append( float(parts[3]))
        #data264.append( float(parts[3]))

with open('ravelresultsall32.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bdata16.append( float(parts[0]))
        bdata32.append( float(parts[1]))
        bdata64.append( float(parts[2]))
        
        #bdata264.append( float(parts[3]))


with open('Postergavelresults32all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        bdata216.append( float(parts[2]))
        bdata232.append( float(parts[3]))
        #data264.append( float(parts[3]))        


with open('ravelresultsall64.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        cdata16.append( float(parts[0]))
        cdata32.append( float(parts[1]))
        cdata64.append( float(parts[2]))
        
        #cdata264.append( float(parts[3]))


with open('Postergavelresults64all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        cdata216.append( float(parts[2]))
        cdata232.append( float(parts[3]))
        #data264.append( float(parts[3]))    





data216 = np.array(data216)
data232 = np.array(data232)
filtereddata216 = data216[~is_outlier(data216)]
filtereddata232 = data232[~is_outlier(data232)]

bdata216 = np.array(bdata216)
bdata232 = np.array(bdata232)
filteredbdata216 = bdata216[~is_outlier(bdata216)]
filteredbdata232 = bdata232[~is_outlier(bdata232)]

cdata216 = np.array(cdata216)
cdata232 = np.array(cdata232)
filteredcdata216 = cdata216[~is_outlier(cdata216)]
filteredcdata232 = cdata232[~is_outlier(cdata232)]


data16 = np.array(data16)
data32 = np.array(data32)
data64 = np.array(data64)
filtereddata16 = data16[~is_outlier(data16)]
filtereddata32 = data32[~is_outlier(data32)]
filtereddata64 = data64[~is_outlier(data64)]

bdata16 = np.array(bdata16)
bdata32 = np.array(bdata32)
bdata64 = np.array(bdata64)
filteredbdata16 = bdata16[~is_outlier(bdata16)]
filteredbdata32 = bdata32[~is_outlier(bdata32)]
filteredbdata64 = bdata64[~is_outlier(bdata64)]

cdata16 = np.array(cdata16)
cdata32 = np.array(cdata32)
cdata64 = np.array(cdata64)
filteredcdata16 = cdata16[~is_outlier(cdata16)]
filteredcdata32 = cdata32[~is_outlier(cdata32)]
filteredcdata64 = cdata64[~is_outlier(cdata64)]





A= [filtereddata216,filtereddata16]
B=[filtereddata232,filtereddata32]
C=[data264,data64]

bA= [filteredbdata216,filteredbdata16]
bB=[filteredbdata232,filteredbdata32]
bC=[bdata264,filteredbdata64]


cA= [filteredcdata216,filteredcdata16]
cB=[filteredcdata232,filteredcdata32]
cC=[cdata264,filteredcdata64]
        #data232.append( float(parts[3]))

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))

bp = axes[0].boxplot(A, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[0].boxplot(B, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[0].boxplot(C, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColorsspe(bp)

bp = axes[1].boxplot(bA, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[1].boxplot(bB, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[1].boxplot(bC, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColorsspe(bp)



bp = axes[2].boxplot(cA, positions = [1, 2], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# second boxplot pair
bp = axes[2].boxplot(cB, positions = [4, 5], widths = 0.6,patch_artist=True)
setBoxColors(bp)

# thrid boxplot pair
bp = axes[2].boxplot(cC, positions = [7, 8], widths = 0.6,patch_artist=True)
setBoxColorsspe(bp)




axes[0].set_title('Fat tree 16')
axes[1].set_title('Fat tree 32')
axes[2].set_title('Fat tree 64')
axes[1].set_yscale('log')
axes[0].set_yscale('log')
#axes[1].get_yaxis().set_ticks([])
axes[2].set_yscale('log')
axes[0].set_ylabel('Time (ms)',size = 30)
axes[1].set_xlabel('Routing Application',size = 30,weight="bold")
for ax in axes:
    ax.yaxis.grid(True)
    #ax.set_xticks([y+1 for y in range(len(alldata))])
    
    
    ax.set_ylim([0,1000])
    ax.set_xlim([0,9])
    ax.set_xticks([1.5, 4.5, 7.5])
    ax.set_xticklabels(['Path \nCalculation', 'Path \nWriting', 'Ports \nExtraction'])
    
for tic in axes[1].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
    
for tic in axes[2].yaxis.get_major_ticks():
    tic.label1On = tic.label2On = False
# set axes limits and labels





'''
data216 = np.array(data216)
data232 = np.array(data232)
filtereddata216 = data216[~is_outlier(data216)]
filtereddata232 = data232[~is_outlier(data232)]
# generate some random test data
alldata = [data16,filtereddata216,data32,filtereddata232,data64]

bdata216 = np.array(bdata216)
bdata232 = np.array(bdata232)
filteredbdata216 = bdata216[~is_outlier(bdata216)]
filteredbdata232 = bdata232[~is_outlier(bdata232)]
# generate some random test bdata
allbdata = [bdata16,filteredbdata216,bdata32,filteredbdata232,bdata64]





# plot violin plot
bp = axes[0].boxplot(alldata,notch=0, sym='+', vert=1, whis=1.5,patch_artist=True)
axes[0].set_title('Gavel vs Ravel Fattree 16')

# plot box plot
bp2 = axes[1].boxplot(allbdata,notch=0, sym='+', vert=1, whis=1.5,patch_artist=True)
axes[1].set_title('Gavel vs Ravel Fattree 32')
axes[1].set_yscale('log')
axes[0].set_yscale('log')
# adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(True)
    #ax.set_xticks([y+1 for y in range(len(alldata))])
    ax.set_xlabel('Routing application')
    ax.set_ylabel('Time (ms)')
    ax.set_ylim([0,80])
    ax.set_xticks([1.5, 4.5, 7.5])
'''
hB, = axes[0].plot([0,0],'g-')
hR, = axes[0].plot([0,0],'r-')
legend((hB, hR),('Gavel', 'Ravel'))
hB.set_visible(False)
hR.set_visible(False)
plt.tight_layout()
plt.subplots_adjust(bottom=0.1)

plt.show()
