import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes
#from neo4j.v1.result import BoltStatementResultSummary
from scipy.stats import ttest_ind, ttest_ind_from_stats,mannwhitneyu
from scipy.special import stdtr
import os
#plt.rcParams.update({'font.size': 40, 'legend.fontsize': 30,'font.color': '#77933C', 'xtick.major.pad':25, 'legend.linewidth': 2})



g3 = []
g4=[]
g5=[]
g6=[]
g7=[]
g8=[]

allavgofarrays = [[] for n in range(10)]

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
    setp(bp['caps'][0], color='red')
    setp(bp['caps'][0], color='red')
    setp(bp['whiskers'][0], color='red')
    setp(bp['whiskers'][0], color='red')
    setp(bp['fliers'][0], color='red')
    setp(bp['fliers'][0], color='red')
    setp(bp['medians'][0], color='red')

    setp(bp['boxes'][1], color='green')
    setp(bp['caps'][1], color='green')
    setp(bp['caps'][1], color='green')
    setp(bp['whiskers'][1], color='green')
    setp(bp['whiskers'][1], color='green')
    setp(bp['fliers'][1], color='green')
    setp(bp['fliers'][1], color='green')
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
fixed
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



def writeallavg(topologyname,parry):
    with open('allavgJournalGavel%sslice.txt' %topologyname, "wb") as myfile:
        for n in parry:
            myfile.write(str (n) + ' ')
        myfile.write('\n')

def writeall(sizeoffattree,arrayofarray):
    fo = open("JournalGavel%sslicesavgofavgtocorrectpvalue.txt" %sizeoffattree, "wb")
    for a in arrayofarray:
        for n in a:

            fo.write(str(n)+'\t')

        fo.write("\n")
    fo.close()

def avgofdelays(delays, cluster):
    if (cluster == 2):
        #print delays,delays[:len(delays)/2],delays[len(delays)/2:]
        return [0.5 *(x + y) for x, y in zip(delays[:len(delays)/2], delays[len(delays)/2:])]
    elif(cluster == 3 ):
        return [0.3333 *(x + y+ z) for x, y,z  in zip(delays[:len(delays)/3], delays[len(delays)/3:2*len(delays)/3],delays[2*len(delays)/3:])]
    elif (cluster== 4):
        pass
def file_len(fname):
    return sum(1 for line in open(fname))
                
def iteratetoplot(topologyname):
    print file_len('JournalGavel%sslicesavgdelay.txt' %topologyname)
    g = [[] for n in range(file_len('JournalGavel%sslicesavgdelay.txt' %topologyname))]
    avgready = [[] for n in range(file_len('JournalGavel%sslicesavgdelay.txt' %topologyname))]
    gslicezero = []
    gsliceone = []
    listofsliceswithvalues= [[] for n in range(10)]
    with open('JournalGavel%sslice.txt' %topologyname) as inf:
        for line in inf:
            parts = line.split("\t") # split line into parts
            if int(parts[3].rstrip()) == 0 :
                gslicezero.append(float (parts[2]))
            if int(parts[3].rstrip()) == 1 :
                gsliceone.append(float (parts[2]))
    listofsliceswithvalues[0] = gslicezero
    listofsliceswithvalues[1] =gsliceone#adding slice 1 resutls without change
    #print gslicezero,gsliceone

    slice = 0 
    with open('JournalGavel%sslicesavgdelay.txt' %topologyname) as inf:
        for line in inf:
            parts = line.split("\t") # split line into parts
            
            for p in parts:
                if p == '\n':
                    pass
                else:
                    #print slice, p
                    g[slice].append(float (p))
            slice = slice +1
    #print len(g)
    oldindex = 1
    for index in xrange(1,9):
        
        #print index
        slicevalues = []
        for hostpairs in g:
            #print len(hostpairs)
            #print oldindex,oldindex+index
            slicevalues.append(np.mean(hostpairs[oldindex:oldindex+index]))
            
        #print slicevalues
        listofsliceswithvalues[index+1] = (slicevalues)
        #print oldindex,oldindex+index
        oldindex = oldindex+index+1
    pvaluearray = []
    ## now arrange all arays to contain all values correctly you need 10 arrays.
    for n in xrange(1, 10,1):
        #print n
        #print len(listofsliceswithvalues[0]),len(listofsliceswithvalues[n])
        #if n == 9:
            #print listofsliceswithvalues[0],'\n',listofsliceswithvalues[n]
        t,p =  mannwhitneyu(listofsliceswithvalues[0],listofsliceswithvalues[n],alternative="less")
        pvaluearray.append( p)
        print "t = " , t," p = " , p,"\n"

    
            
    writeallavg(topologyname,pvaluearray)
    writeall(topologyname,listofsliceswithvalues)
    

   
for i in range(1):
    #os.system("python testslicing.py")
    #for t in ['Geant2012','16','32']:
    iteratetoplot("Geant2012")


# index = np.arange(10)
# plt.bar(index, finalavg, 0.5,
#                  alpha=0.4,
#                  color='g')
# 
# plt.xlabel('No. of Slices')
# plt.ylabel('Time (ms)')
# plt.title('Geant2012')
# plt.xticks(index  , ('0', '1', '2', '3', '4','5', '6', '7','8','9'))
# plt.legend()
# 
# #plt.tight_layout()
# #plt.show()

