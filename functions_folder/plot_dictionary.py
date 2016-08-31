import matplotlib.pyplot as plt

def plot_dictionary(D):
    if "no_chi_test" in D:
        D.pop("no_chi_test")
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    plt.show()


"""


def histogram_from_vector(bins_cluster,distributions):
    n,bins,patches = plt.hist(bins_cluster, bins=range(0,len(distributions)+1,1))
    #plt.show()
    return n, bins, patches

#plt.hist(bins_cluster["gap_90"], bins=range(0,len(distributions["gap_90"])+1,1))



"""
