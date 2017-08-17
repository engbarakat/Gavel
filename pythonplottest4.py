import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


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




# make up some fake data
pos_mut_pcts = np.array([np.median(data216), np.median(bdata216), np.median(cdata216)])
pos_cna_pcts = np.array([np.median(data232),np.median(bdata232),np.median(cdata232)])
pos_both_pcts = np.array([0, 0, 0])
neg_mut_pcts = np.array([np.median(data16),np.median(bdata16), np.median(cdata16)])
neg_cna_pcts = np.array([np.median(data32), np.median(bdata232), np.median(cdata32)])
neg_both_pcts = np.array([np.median(data64),np.median(bdata64), np.median(cdata64)])
genes = ['16', '32', '64']

with sns.axes_style("white"):
    sns.set_style("ticks")
    sns.set_context("talk")

    # plot details
    bar_width = 0.35
    epsilon = .015
    line_width = 1
    opacity = 0.7
    pos_bar_positions = np.arange(len(pos_mut_pcts))
    neg_bar_positions = pos_bar_positions + bar_width

    # make bar plots
    hpv_pos_mut_bar = plt.bar(pos_bar_positions, pos_mut_pcts, bar_width,
                              color='#ED0020',
                              label='PC Gavel')
    hpv_pos_cna_bar = plt.bar(pos_bar_positions, pos_cna_pcts, bar_width-epsilon,
                              bottom=pos_mut_pcts,
                              alpha=opacity,
                              color='white',
                              edgecolor='#ED0020',
                              linewidth=line_width,
                              hatch='//',
                              label='PW Gavel')
    '''hpv_pos_both_bar = plt.bar(pos_bar_positions, pos_both_pcts, bar_width-epsilon,
                               bottom=pos_cna_pcts+pos_mut_pcts,
                               alpha=opacity,
                               color='white',
                               edgecolor='#ED0020',
                               linewidth=line_width,
                               hatch='0',
                               label='HPV+ Both')'''
    hpv_neg_mut_bar = plt.bar(neg_bar_positions, neg_mut_pcts, bar_width,
                              color='#0000DD',
                              label='PC Ravel')
    hpv_neg_cna_bar = plt.bar(neg_bar_positions, neg_cna_pcts, bar_width-epsilon,
                              bottom=neg_mut_pcts,
                              color="white",
                              hatch='//',
                              edgecolor='#0000DD',
                              ecolor="#0000DD",
                              linewidth=line_width,
                              label='PW Ravel')
    hpv_neg_both_bar = plt.bar(neg_bar_positions, neg_both_pcts, bar_width-epsilon,
                               bottom=neg_cna_pcts+neg_mut_pcts,
                               color="white",
                               hatch='0',
                               edgecolor='#0000DD',
                               ecolor="#0000DD",
                               linewidth=line_width,
                               label='PE Ravel')
    plt.xticks(neg_bar_positions, genes, rotation=45)
    plt.ylabel('Time (ms)')
    plt.legend(loc='best')
    sns.despine()