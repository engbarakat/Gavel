import matplotlib.pyplot as plt
import numpy as np

# Random test data
def cdf(data):

    data_size=len(data)

    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    # Plot the cdf
    plt.plot(bin_edges[0:-1], cdf,linestyle='-', color='g')
    plt.ylim((0,1))
    plt.ylabel("CDF")
    plt.grid(True)
    plt.xlabel("Time (ms)")

    plt.show()





data = []
data2=[]
with open('gavelresults16all.txt') as inf:
    for line in inf:
        parts = line.split("	") # split line into parts
        data.append( float(parts[2]))
        data2.append( float(parts[3]))

cdf(data)
cdf(data2)
