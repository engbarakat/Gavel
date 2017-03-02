import matplotlib.pyplot as plt
import numpy as np

data64 = []
data264=[]
with open('gavelresults64all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        data64.append( float(parts[2]))
        if float(parts[2]) >12:
			print parts[2]
        data264.append( float(parts[3]))

data32 = []
data232=[]
with open('gavelresults32all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        data32.append( float(parts[2]))
        if float(parts[2]) >12:
			print parts[2]
        data232.append( float(parts[3]))
        
data16 = []
data216=[]
with open('gavelresults16all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        data16.append( float(parts[2]))
        if float(parts[2]) >12:
			print parts[2]
        data216.append( float(parts[3]))

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

# generate some random test data
alldata = [data16,data32,data64]
alldata2=  [data216,data232,data264]

# plot violin plot
axes[0].boxplot(alldata)
axes[0].set_title('Get Path')

# plot box plot
axes[1].boxplot(alldata2)
axes[1].set_title('Writes Path')
axes[1].set_yscale('log')
axes[0].set_yscale('log')
# adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(True)
    ax.set_xticks([y+1 for y in range(len(alldata))])
    ax.set_xlabel('Fat Tree sizes')
    ax.set_ylabel('Time (ms)')

# add x-tick labels
plt.setp(axes, xticks=[y+1 for y in range(len(alldata))],
         xticklabels=['16', '32', '64'])
plt.show()
