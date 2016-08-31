import math
import numpy as np

def determine_child_bins(bins_cluster,P, messages_count, gap_vector,pops):
    if len(P)==0:
        return [],[]
    elif len(P) >= pops: ####!!!!
        take_out_first_elements(pops,P)  ###!!
    #    print("pop")
    #elif len(P) > 3: ####!!!!
    #    take_out_first_elements(pops,P)  ###!!!
    real_bad_bins = []
    bad_parents_of_this_bin=[]
    first_bad = True
    writing = False
    for m in range(messages_count-max(gap_vector)-1):
        bins_of_m = get_bins_of_m(m,gap_vector) # get in what bins is m
        parents_of_m = get_parents_of_m(bins_of_m, bins_cluster,gap_vector) # get the parents distributions of m
        has_bad_parents, bad_parents_indeces = check_m_parents(parents_of_m, P) # check if the parents are in the pool of bad parents and get indeces of bad parents
        if has_bad_parents:
            if first_bad:
                left = m
                first_bad = False
                previous = m
                writing = True
                previous_parents=parents_of_m
                continue
            if writing == False:
                left = m
                previous = m
                writing = True
                previous_parents=parents_of_m
                continue
            if m == previous + 1:
                previous = m
                writing = True
                previous_parents=parents_of_m
                continue
            #else:
            #    real_bad_bins.append([left, previous])
            #    writing = False
        else:
            if writing:
                real_bad_bins.append([left+1,previous+1 ])
                bad_parents_of_this_bin.append(previous_parents)
                writing = False
            else:
                continue
    if m == messages_count-max(gap_vector)-1: #was 200
        if writing:
            real_bad_bins.append([left+1,previous+1 ])
            bad_parents_of_this_bin.append(previous_parents)
    return real_bad_bins, bad_parents_of_this_bin

def take_out_first_elements(pops, P): # the first elements of P may be normal message but they appear because the algorithm is learning
    for i in range(1,pops+1):
        P.pop(0)


def get_bins_of_m(m,gap_vector): # given a message it returns the bins it is in
    bins=[]
    for gap in gap_vector:
        bins.append( math.floor( m / gap) )
    return bins

def get_parents_of_m(bins_of_m,bins_cluster,gap_vector): # gets the parent distributions of the bins
    p = []
    b_index = 0
    for gap in gap_vector:
        p.append( bins_cluster["gap_"+str(gap)][ bins_of_m[b_index] ] )
        b_index += 1
    return p

def check_m_parents(parents_of_m, P):
    bad_parents_indeces = []
    if P == []:
        return False, []
    for i in range(len(P)):
        if parents_of_m in P[i]:#if np.any(parents_of_m in P[i]):
            bad_parents_indeces.append(P[i])
    if len(bad_parents_indeces)==0:
        return False, []
    else:
        return True, bad_parents_indeces
