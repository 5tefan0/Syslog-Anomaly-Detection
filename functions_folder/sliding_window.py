#------------------------------------------------------------------------------#
# Sliding window statistics
#------------------------------------------------------------------------------#
import scipy
import numpy as np
import math
from scipy.stats import itemfreq


#------------------------------------------------------------------------------#
def create_chi_tests_count(gap,chi_tests_count):
    for G in gap:
        g=str(G)
        chi_tests_count["window_chi_ineffective"+str(g)]=0
        chi_tests_count["window_chi_effective_same"+str(g)]=0
        chi_tests_count["window_chi_effective_different"+str(g)]=0
#------------------------------------------------------------------------------#
def create_flags(gap, flags):
    for G in gap:
        g=str(G)
        flags["bin_chi_different"+str(G)]=[]
        flags["bin_number_chi_different"+str(G)]=[]
        flags["bin_chi_ineffective"+str(G)]=[]
        flags["bin_number_chi_ineffective"+str(G)]=[]
#------------------------------------------------------------------------------#
def create_distributions(gap, distributions):
    for G in gap:
        g=str(G)
        distributions["gap_"+str(G)]=[]
#------------------------------------------------------------------------------#
def create_bins(gap, bins_cluster):
    for G in gap:
        g=str(G)
        bins_cluster["gap_"+str(G)]=[]
#------------------------------------------------------------------------------#

def create_parents_distribution(parents_distribution):
    parents_distribution["different_left"]=[]
    parents_distribution["different_right"]=[]
    parents_distribution["different_father"]=[]
    parents_distribution["different_mother"]=[]
    parents_distribution["ineffective_left"]=[]
    parents_distribution["ineffective_right"]=[]
    parents_distribution["ineffective_father"]=[]
    parents_distribution["ineffective_mother"]=[]

#------------------------------------------------------------------------------#
def create_bins_counter(gap,bins_count):
    for G in gap:
        g=str(G)
        bins_count["gap_"+str(G)]=0


"""

def sliding_window_flags_eff(flags,messages_count,M_T, gap_vector, chi_tests_count,storage_fifty):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 200 and messages_count %  gap == 0:# and messages_count < 1501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            for comparing_window in storage_fifty:
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.01: #the distributions are the same
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    if effective_different:
                        ineffective = False
                    else:
                        ineffective = True
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
                continue
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
                flags["bin_chi_different"+str(gap)].append(messages_count)
                storage_fifty.append(itemfreq(M_T[messages_count-gap:messages_count]))
                continue
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
                flags["bin_chi_ineffective"+str(gap)].append(messages_count)
                storage_fifty.append(itemfreq(M_T[messages_count-gap:messages_count]))
                continue
            else:
                assert(False)

        #else:
            #chi_test_count["no_chi_test"+str(g)] +=1

#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#


def sliding_window_flags_eff_new(flags,messages_count,M_T, gap_vector, chi_tests_count, distributions,bins_cluster):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 200 and messages_count % gap == 0:# and messages_count < 1501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            window_count=0
            for comparing_window in distributions["gap_"+str(gap)]:
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.01: #the distributions are the same
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    if effective_different:
                        ineffective = False
                    else:
                        ineffective = True
                window_count += 1
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
                bins_cluster["gap_"+str(gap)].append(window_count)
                continue
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
                flags["bin_chi_different"+str(gap)].append(messages_count)
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                continue
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
                flags["bin_chi_ineffective"+str(gap)].append(messages_count)
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                continue
            else:
                assert(False)

        #else:
            #chi_test_count["no_chi_test"+str(g)] +=1

#------------------------------------------------------------------------------#




"""
#------------------------------------------------------------------------------#

def reindexing_bins_cluster(bins_cluster, distributions, gap_vector): #since the bins restart indexing when changing gap, here we reindex to have a different index for all bins
    number_of_bins = []
    for gap in gap_vector:
        if len(number_of_bins) > 0:
            for i in range(0,len(bins_cluster["gap_"+str(gap)])):
                bins_cluster["gap_"+str(gap)][i] += sum(number_of_bins)
        number_of_bins.append(len(distributions["gap_"+str(gap)]))




#------------------------------------------------------------------------------#



#------------------------------------------------------------------------------#
def sliding_window_flags_eff_new(flags,messages_count,M_T, gap_vector, chi_tests_count, distributions,bins_cluster,bins_count):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 0 and messages_count % gap == 0:# and messages_count < 1501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            window_count=0
            for comparing_window in distributions["gap_"+str(gap)]:
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        #print("same_len,same_items")
                        #print(itemfreq(M_T[messages_count-gap:messages_count])[:,0])
                        #print(comparing_window[:,0])
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.1: #the distributions are the same
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    if effective_different:
                        ineffective = False
                    else:
                        ineffective = True
                window_count += 1
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
                flags["bin_chi_different"+str(gap)].append(messages_count)
                flags["bin_number_chi_different"+str(gap)].append(bins_count["gap_"+str(gap)])
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
                flags["bin_chi_ineffective"+str(gap)].append(messages_count)
                flags["bin_number_chi_ineffective"+str(gap)].append(bins_count["gap_"+str(gap)])
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            else:
                assert(False)

        #else:
            #chi_test_count["no_chi_test"+str(g)] +=1

#------------------------------------------------------------------------------#



def analyze_flagged_bin(flags):
    #get bin size
    for end_bin in flags["bin_chi_different150"]:
        M_T[end_bin - bin_size: end_bin] #templates appeared
       # itemfreq(M_T[400:450])[:,1] < 2
       # then compare with rest itemfreq of whole M_T # then rare item

"""

# Keep in memory the contingency table for every 50 messages
def store_frequencies(sf):
    sf.append(itemfreq(M_T[messages_count-gap:messages_count])[:,0])



#------------------------------------------------------------------------------#

def sliding_window_gaps(messages_count,M_T,chi_test_count):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in [50,100,300,1000]:
        if messages_count > 1000 and messages_count % 50 == 0:# and messages_count < 5501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,0]):
                if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,0]):
                    a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,1])
                    if b > 0.05:
                        #print("The chi square was effective. The bins have the same distribution. \n")
                        #chi_test_count2[2]+=1
                        chi_test_count["window_chi_effective_same"]+=1
                    else:
                        #print("The chi square was effective. The bins do NOT have the same distribution. p-value is {0} \n".format(b))
                        #chi_test_count2[3]+=1
                        chi_test_count["window_chi_effective_different"] +=1
                else:
                    #print("Same lenght but different items")
                    #chi_test_count2[1]+=1
                    chi_test_count["window_chi_different"] +=1
            else:
                #print("The chi square test would be ineffective. Some rare event appeared. \n")
                #chi_test_count2[0]+=1
                chi_test_count["window_chi_ineffective"] +=1
                continue
        else:
            chi_test_count["no_chi_test"] +=1

#------------------------------------------------------------------------------#
def sliding_window_gaps(messages_count,M_T):
    for gap in [50,100,300,1000]:
        if messages_count > 1000 and messages_count % 50 == 0 and messages_count < 7501:
            DoChiSquare = False
            HowManyWindows = math.floor(messages_count/gap)
            previousH=1
            for H in numpy.linspace(2,HowManyWindows,HowManyWindows-1):
                if len(itemfreq(M_T[messages_count-gap*previousH:messages_count])[:,0]) == len(itemfreq(M_T[messages_count-(gap*H):messages_count-(gap*previousH+1)])[:,0]) and np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == itemfreq(M_T[messages_count-(gap*H):messages_count-(gap*previousH+1)])[:,0]):
                    DoChiSquare = True
                    previousH=H
                else:
                    previousH=H
                    chi_test_count["window_chi_ineffective"] +=1
                    continue
                if DoChiSquare:
                    a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap*previousH:messages_count])[:,1],f_exp=itemfreq(M_T[messages_count-(gap*H):messages_count-(gap*previousH+1)])[:,1])
                    if b > 0.05:
                        #print("The chi square was effective. The bins have the same distribution. \n")
                        #chi_test_count2[2]+=1
                        chi_test_count["window_chi_effective_same"]+=1
                    else:
                        #print("The chi square was effective. The bins do NOT have the same distribution. p-value is {0} \n".format(b))
                        #chi_test_count2[3]+=1
                        chi_test_count["window_chi_effective_different"] +=1
                else:
                    #print("Same lenght but different items")
                    #chi_test_count2[1]+=1
                    chi_test_count["window_chi_different"] +=1
            #else:
            #chi_test_count["no_chi_test"] +=1



# This stores ALL the distributions! ineffeicient

def sliding_window_flags(flags,messages_count,M_T, gap_vector, chi_tests_count,storage_fifty):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 200 and messages_count % gap == 0:# and messages_count < 1501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            for comparing_window in storage_fifty:
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.01:
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    ineffective = True
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
                flags["bin_chi_different"+str(gap)].append(messages_count)
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
                flags["bin_chi_ineffective"+str(gap)].append(messages_count)
            else:
                assert(False)
            storage_fifty.append(itemfreq(M_T[messages_count-gap:messages_count]))
        #else:
            #chi_test_count["no_chi_test"+str(g)] +=1

"""

"""
def sliding_window(messages_count,M_T,chi_test_count):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    gap=50
    if messages_count >= 100 and messages_count % 33 == 0 and messages_count < 7501: #### when to do the test
        # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,0]):
            if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,0]):
                a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=itemfreq(M_T[messages_count-(gap*2):messages_count-(gap+1)])[:,1])
                if b > 0.01:
                    #print("The chi square was effective. The bins have the same distribution. \n")
                    #chi_test_count2[2]+=1
                    chi_test_count["window_chi_effective_same"]+=1
                else:
                    #print("The chi square was effective. The bins do NOT have the same distribution. p-value is {0} \n".format(b))
                    #chi_test_count2[3]+=1
                    chi_test_count["window_chi_effective_different"] +=1
            else:
                #print("Same lenght but different items")
                #chi_test_count2[1]+=1
                chi_test_count["window_chi_different"] +=1
        else:
            #print("The chi square test would be ineffective. Some rare event appeared. \n")
            #chi_test_count2[0]+=1
            chi_test_count["window_chi_ineffective"] +=1
    else:
        chi_test_count["no_chi_test"] +=1

#------------------------------------------------------------------------------#


def sliding_window_A(messages_count,M_T, gap_vector, chi_tests_count,storage_fifty):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 100 and messages_count % gap == 0:# and messages_count < 1501: #### when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            for comparing_window in storage_fifty:
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.01:
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    ineffective = True
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
            else:
                assert(False)
            storage_fifty.append(itemfreq(M_T[messages_count-gap:messages_count]))
        #else:
            #chi_test_count["no_chi_test"+str(g)] +=1
"""
#------------------------------------------------------------------------------#
def sliding_window_flags_eff_new_x(flags,messages_count,M_T, gap_vector, chi_tests_count, distributions,bins_cluster,bins_count):#,window_chi_ineffective, window_chi_different, window_chi_effective_same, window_chi_effective_different):
    for gap in gap_vector:
        if messages_count > 0 and messages_count % gap == 0:#  when to do the test
            # the length of the frequencies vector must be the same otherwise there are not enough data for a chi squared test
            ineffective=True
            effective_same=False
            effective_different=False
            window_count=0
            l = len(itemfreq(M_T[messages_count-gap:messages_count]))
            for comparing_window in distributions["gap_"+str(gap)]:
                for i in range(l):
                    if itemfreq(M_T[messages_count-gap:messages_count])[i][1] < 5:
                        ineffective = True
                        break
                if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == len(comparing_window[:,0]):
                    if np.all(itemfreq(M_T[messages_count-gap:messages_count])[:,0] == comparing_window[:,0]):
                        #print("same_len,same_items")
                        #print(itemfreq(M_T[messages_count-gap:messages_count])[:,0])
                        #print(comparing_window[:,0])
                        if len(itemfreq(M_T[messages_count-gap:messages_count])[:,0]) == 1: #this needs a special case because the chi square doesn't work with only one category
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        a,b=scipy.stats.chisquare(itemfreq(M_T[messages_count-gap:messages_count])[:,1],f_exp=comparing_window[:,1])
                        if b > 0.1: #the distributions are the same
                            ineffective = False
                            effective_different = False
                            effective_same = True
                            break
                        else:
                            effective_different=True
                            ineffective = False
                    else:
                        if effective_different:
                            ineffective = False
                        else:
                            ineffective = True
                else:
                    if effective_different:
                        ineffective = False
                    else:
                        ineffective = True
                window_count += 1
            if effective_same:
                chi_tests_count["window_chi_effective_same"+str(gap)]+= 1
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            elif effective_different:
                chi_tests_count["window_chi_effective_different"+str(gap)] += 1
                flags["bin_chi_different"+str(gap)].append(messages_count)
                flags["bin_number_chi_different"+str(gap)].append(bins_count["gap_"+str(gap)])
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            elif ineffective:
                chi_tests_count["window_chi_ineffective"+str(gap)] +=1
                flags["bin_chi_ineffective"+str(gap)].append(messages_count)
                flags["bin_number_chi_ineffective"+str(gap)].append(bins_count["gap_"+str(gap)])
                distributions["gap_"+str(gap)].append(itemfreq(M_T[messages_count-gap:messages_count]))
                bins_cluster["gap_"+str(gap)].append(window_count)
                bins_count["gap_"+str(gap)]+=1
                continue
            else:
                assert(False)
