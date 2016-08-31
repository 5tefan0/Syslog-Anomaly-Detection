#------------------------------------------------------------------------------#
# Input: indeces of anomalous messages
# Output: [ interval[a,b]  ] vector of bins
#------------------------------------------------------------------------------#
import numpy as np
from scipy.stats import itemfreq
from functools import reduce

def determine_anomalous_bins(indeces):
    bins=[]
    if len(indeces)==0:
        print("No bins to create")
        return bins
    left_extreme = indeces[0] # set the first left extreme of the first bin
    for i in range(len(indeces)-1):
        if indeces[i]==indeces[i+1]-1:
            continue
        else:
            #indeces[i] was extreme of the interval
            bins.append([ left_extreme , indeces[i] ])
            left_extreme = indeces[i+1]
    bins.append([ left_extreme , indeces[i] + 1 ])
    return bins

#------------------------------------------------------------------------------#

def determine_anomalous_bins_parents(indeces,parents_distribution,chi_result):
    bins=[]
    bins_parents=[]
    if len(indeces)==0:
        print("No bins to create")
        return bins, bins_parents
    left_extreme = indeces[0] # set the first left extreme of the first bin
    for i in range(len(indeces)-1):
        if indeces[i]==indeces[i+1]-1:
            continue
        else:
            #indeces[i] was extreme of the interval
            bins.append([ left_extreme , indeces[i] ])
            bins_parents.append(determine_bin_parents_NR(left_extreme,indeces[i],parents_distribution,chi_result)) #use NR version to keep bins separated
            left_extreme = indeces[i+1]
    bins.append([ left_extreme , indeces[i] + 1 ]) # append last bin
    bins_parents.append(determine_bin_parents_NR(left_extreme,indeces[i]+1,parents_distribution,chi_result)) # aggiunto NR
    return bins , bins_parents

def determine_bin_parents(A,B,parents_distribution,chi_result):
    parents=[]
    X=parents_distribution[chi_result+"_left"]
    Y=parents_distribution[chi_result+"_right"]
    y_counter = 0
    x_counter = 0
    for y in Y:
        if A > y:
            y_counter += 1
            x_counter += 1
            continue
        else:
            if B < X[x_counter]:
                break
            else:
                parents.append([parents_distribution[chi_result+"_father"][x_counter],parents_distribution[chi_result+"_mother"][y_counter]])
                x_counter += 1
                y_counter += 1
    if len(parents)==0:
        assert(False)
    else:
        return list(reduce(np.union1d,parents))

def determine_bin_parents_NR(A,B,parents_distribution,chi_result): #this version keeps the bins separated
    parents=[]
    X=parents_distribution[chi_result+"_left"]
    Y=parents_distribution[chi_result+"_right"]
    y_counter = 0
    x_counter = 0
    for y in Y:
        if A > y:
            y_counter += 1
            x_counter += 1
            continue
        else:
            if B < X[x_counter]:
                break
            else:
                parents.append([parents_distribution[chi_result+"_father"][x_counter],parents_distribution[chi_result+"_mother"][y_counter]])
                x_counter += 1
                y_counter += 1
    if len(parents)==0:
        assert(False)
    else:
        return parents




"""
    parents_distribution["different_left"]=[]
    parents_distribution["different_right"]=[]
    parents_distribution["different_father"]=[]
    parents_distribution["different_mother"]=[]
    parents_distribution["ineffective_left"]=[]
    parents_distribution["ineffective_right"]=[]
    parents_distribution["ineffective_father"]=[]
    parents_distribution["ineffective_mother"]=[] """

#------------------------------------------------------------------------------#

# This works just the same but to create the bins you look backwards
def determine_anomalous_bins2(indeces):
    bins=[]
    for i in range(len(indeces)):
        if i == 0:
            left_extreme = indeces[i]
            continue
        if indeces[i]==indeces[i-1]+1:
            continue
        else:
            #indeces[i] was extreme of the interval
            bins.append([ left_extreme , indeces[i-1] ])
            left_extreme = indeces[i]
    bins.append([ left_extreme , indeces[i] ])
    return bins


#------------------------------------------------------------------------------#

def anomalous_bins_frequencies(M_T,bins):
    frequencies = []
    for i in range(len(bins)):
        frequencies.append(itemfreq(M_T[bins[i][0]:bins[i][1]]))
    return frequencies

#------------------------------------------------------------------------------#
