#------------------------------------------------------------------------------#
# Given two lists of intervals it returns the list of overlapping integer points
#------------------------------------------------------------------------------#

import numpy as np
from functools import reduce

#chi result either "different" or "ineffective"
"""
# only if gap_vector has two elements
def find_overlapping_indeces(flags,gap_vector,chi_result): #small e large li prendi dal flag
    small_x = flags["bin_chi_"+ chi_result+str(gap_vector[0])]
    large_y = flags["bin_chi_"+ chi_result+str(gap_vector[1])]
    suspects = []
    for x in small_x:
        new_x=[ x - gap_vector[0] +1,x]
        for y in large_y:
            new_y = [y - gap_vector[1]+1,y]
            if new_x[1] < new_y[0]:
                break
            elif new_x[0] > new_y[1]:
                continue
            else:# x[1] >= y[0] and x[0] <= y[1]:
                 suspects.append(list(range(max(new_x[0], new_y[0]), min(new_x[-1], new_y[-1])+1)))
    sus=np.hstack(suspects)
    return  sus
"""

"""

# if gap_vector has more than two elements:
def find_overlapping_indeces_new(flags,gap_vector,chi_result): #small e large li prendi dal flag
    coupled=[] # first we find overlapping indeces in couples , later we look at the common elements
    for a in range(len(gap_vector)-1):
        small_x = flags["bin_chi_"+ chi_result+str(gap_vector[a])]
        large_y = flags["bin_chi_"+ chi_result+str(gap_vector[a+1])]
        suspects = []
        for x in small_x:
            new_x=[ x - gap_vector[a] +1,x]
            for y in large_y:
                new_y = [y - gap_vector[a+1]+1,y]
                if new_x[1] < new_y[0]:
                    break
                elif new_x[0] > new_y[1]:
                    continue
                else:# x[1] >= y[0] and x[0] <= y[1]:
                     suspects.append(list(range(max(new_x[0], new_y[0]), min(new_x[-1], new_y[-1])+1)))
        if len(suspects) == 0:
            continue
        else:
            coupled.append(np.hstack(suspects)) # hstack makes flat vector
    if len(coupled) == 0:
        return []
    else:
        return  reduce(np.intersect1d,coupled) #finds common elements among the "coupled intersections"

"""

# if gap_vector has more than two elements:
def find_overlapping_indeces_parents(flags,gap_vector,chi_result,bins_cluster,parents_distribution): #small e large li prendi dal flag
    coupled=[] # first we find overlapping indeces in couples , later we look at the common elements
    for a in range(len(gap_vector)-1):
        small_x = flags["bin_chi_"+ chi_result+str(gap_vector[a])]
        large_y = flags["bin_chi_"+ chi_result+str(gap_vector[a+1])]
        suspects = []
        x_counter = 0
        for x in small_x: # the element of flags["bin_chi_"+ chi_result+str(gap_vector[a])] we are using
            y_counter=0
            new_x=[ x - gap_vector[a] +1,x]
            for y in large_y: # the element of flags["bin_chi_"+ chi_result+str(gap_vector[a+1])] we are using
                new_y = [y - gap_vector[a+1]+1,y]
                if new_x[1] < new_y[0]:
                    break
                elif new_x[0] > new_y[1]:
                    y_counter += 1
                    continue
                else:# x[1] >= y[0] and x[0] <= y[1]:
                     suspects.append(list(range(max(new_x[0], new_y[0]), min(new_x[-1], new_y[-1])+1)))
                     father_distribution = bins_cluster["gap_"+str(gap_vector[a])][flags["bin_number_chi_"+chi_result+str(gap_vector[a])][x_counter]]
                     mother_distribution = bins_cluster["gap_"+str(gap_vector[a+1])][flags["bin_number_chi_"+chi_result+str(gap_vector[a+1])][y_counter]]
                     parents_distribution[chi_result+"_left"].append(max(new_x[0], new_y[0]))
                     parents_distribution[chi_result+"_right"].append(min(new_x[-1], new_y[-1])+1)
                     parents_distribution[chi_result+"_mother"].append(mother_distribution) #make faster
                     parents_distribution[chi_result+"_father"].append(father_distribution)
                     #parents_distribution[""]
            x_counter+=1
        if len(suspects) == 0:
            continue
        else:
            coupled.append(np.hstack(suspects)) # hstack makes flat vector
    if len(coupled) == 0:
        return []
    else:
        return  reduce(np.intersect1d,coupled) #finds common elements among the "coupled intersections" EX: reduce(np.intersect1d,[[1,2,3,4],[2,3]]) -> array([2, 3])
