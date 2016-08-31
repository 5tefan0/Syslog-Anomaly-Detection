# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------#
# Import modules
#------------------------------------------------------------------------------#

# To keep track of time:
import time
t=time.time()

# To clear all variables:
from functions_folder.ClearAllVariables import clear_all

# Classes setup:
from classes_setup import Template

from Functions_for_writing_up_results.write_child import write_vector_of_interval_of_messages

from functions_folder.analyze_bins import analyze_bins_and_write

from functions_folder.sliding_window import create_chi_tests_count, create_flags, create_distributions, create_bins, create_bins_counter, sliding_window_flags_eff_new, sliding_window_flags_eff_new_x, create_parents_distribution, reindexing_bins_cluster

from Functions_for_writing_up_results.write_stuff import write_templates , write_different_distribution_messages, write_chi_ineffective_messages, write_lines#, write_vector_of_interval_of_messages
from functions_folder.set_log_files import set_log_files 
from functions_folder.find_template import find_template, template_vector_to_string
from functions_folder.determine_anomalous_bins import  determine_anomalous_bins_parents, anomalous_bins_frequencies
#from functions_folder.plot_dictionary import plot_dictionary
from functions_folder.find_overlapping_indeces import find_overlapping_indeces_parents 
from functions_folder.determine_child_bins import determine_child_bins

from Functions_to_prepare_datasets_for_D3.viz import template_occurrences, templates_around, write_json_from_list,  write_force_json_from_dictionary
from Functions_to_prepare_datasets_for_D3.viz_distributions import distributions_occurrences, distributions_around, write_json_from_dictionary, index_distributionOcc_freq, write_force_json_from_dictionary_dist

# To create simulated syslog
from Functions_for_simulations.create_syslog import generate_templates, generate_syslog_with_anomalies
from Functions_for_simulations.comparisons import compare, pops_with_threshold




# FOR SIMULATIONS!
#create templates:
#INPUT: number of templates, mean length
#tt=generate_templates(60, 20)
#create syslog: 
#INPUT: number of lines, templates, number of little groups of new templates, number of big groups of old templates with new distribution
c,a,b,artificial_group_anomaly=generate_syslog_with_anomalies(100000,tt,15,3)
#after generating templates and syslog put "simulation" as second parameter of set_log_files (the other parameters do not matter)
#------------------------------------------------------------------------------#
# Clears the variables space from the workspace
#------------------------------------------------------------------------------#
if __name__ == "__main__":
    clear_all()
#------------------------------------------------------------------------------#
    



#------------------------------------------------------------------------------#
# Set the list of log files to analize
#------------------------------------------------------------------------------#
# set syslog to analyze: cloud, type and years. Example: set_log_files("lab","monitor",["2015","2016"]) 
# type of cloud: lab or wide
# type of log files : lab-fs0 (~ 1100 sec), monitor (~ 200 sec), nat (~4300 sec/ 1h), lab-hv00, lab-hv (~ 1094 sec)
address = set_log_files("lab","simulation",["2015"])#,"2016"]) 
#------------------------------------------------------------------------------#

#sim. V=generate_syslog_two_types_of_anomaly(100000, tt, 30, 50) - 

#------------------------------------------------------------------------------#
# Initialization
#------------------------------------------------------------------------------#
messages_count=0
templates=[]
Templates_stats=[]
i=0
M_T=[] #message-template 

examining_file_time=[]

# bin sizes for chi^2 tests
gap_vector=[40,75]

chi_tests_count = {}
create_chi_tests_count(gap_vector,chi_tests_count)
flags = {} # dict.keys(flags) -> dict_keys(['bin_number_chi_different170', 'bin_number_chi_ineffective90', 'bin_chi_ineffective170', 'bin_chi_ineffective90', 'bin_number_chi_ineffective170', 'bin_chi_different90', 'bin_chi_different170', 'bin_number_chi_different90'])
distributions = {} # dict.keys(distributions) ->  dict_keys(['gap_90', 'gap_170'])
bins_cluster = {} # dict.keys(bins_cluster) ->  dict_keys(['gap_90', 'gap_170'])
bins_count = {} # dict.keys(bins_count) -> dict_keys(['gap_90', 'gap_170'])
parents_distribution = {} 
create_parents_distribution(parents_distribution)
create_flags(gap_vector,flags)
create_distributions(gap_vector, distributions)
create_bins(gap_vector, bins_cluster)
create_bins_counter(gap_vector,bins_count)

# We consider a template rare if it appears <= rare_threshold times
rare_threshold = 10


#------------------------------------------------------------------------------#
# Algorithm
#------------------------------------------------------------------------------#


for files in address:
    f = open(files,"r")
    
    file_timer=time.time()
    
    FoundMatching= False
    MoreFiles = False#
    
    print("\n Examining " + f.name + " ...\n")
    
    
    for line in f:
        # Count number of messages analyzed:
        messages_count+=1

        #----------------------------------------------------------------------#
        # Find the template of the current message
        #----------------------------------------------------------------------#
        FoundMatching= False
        
        #Split line into its words
        new_message = line.split()
        i=-1
        for i in range(len(templates)):
            # If a match has NOT been found, keep comparing the line with the templates:
            comparing_template=templates[i]
            if len(comparing_template) != len(new_message):
                    # If the lenghts are different then they are not the same template
                FoundMatching=False
            else:
                # If the lenghts are the same check if there is any matching template (to update):
                FoundMatching=find_template(i,new_message,comparing_template,templates,Templates_stats)
            if FoundMatching == True:
                t_index = i
                # Exit loop if matching template was found:
                break
        # If you never found a match add a new template:
        if FoundMatching==False:
            t_index = i+1
            templates.append(new_message)
            Templates_stats.append(Template(t_index,templates[t_index]))
        #----------------------------------------------------------------------#
        # Now that we have the message and its template we compute statistics
        #----------------------------------------------------------------------#
        Templates_stats[t_index]._counts += 1 
        Templates_stats[t_index]._line_indeces.append(messages_count)
        Templates_stats[t_index]._words = template_vector_to_string(templates[t_index])
        M_T.append(t_index)
        
        #----------------------------------------------------------------------#
        # Use sliding windows that compute CHI SQUARED TESTS to find strange bins of messages
        #----------------------------------------------------------------------#         
        #sliding_window_flags_eff(flags,messages_count, M_T, gap_vector,chi_tests_count,storage_distributions)
        sliding_window_flags_eff_new_x(flags,messages_count, M_T, gap_vector,chi_tests_count,distributions,bins_cluster,bins_count)
        # compute elapsed time for each file
        #examining_file_time.append([len(storage_distributions),time.time()-file_timer])
        

print("\n\n Finding interesting bins of messages ... \n")    
   
# reindexing :   
reindexing_bins_cluster(bins_cluster, distributions, gap_vector)

#----------------------------------------------------------------------#
# Messages that have a distribution different than usual
#----------------------------------------------------------------------#
chi_different_indeces=find_overlapping_indeces_parents(flags,gap_vector,"different",bins_cluster,parents_distribution)#find_overlapping_indeces_new(flags,gap_vector,"different")
chi_different_bins, P_different= determine_anomalous_bins_parents(chi_different_indeces, parents_distribution,"different") #anomalous_distribution_bins= determine_anomalous_bins(different_distribution_indeces)  ###chNGE TO NEW
pops_with_threshold(chi_different_bins,P_different,10000)#take out bad parents if too close to beginning of the algorithm
different_child_bins, bad_parents_of_different_child = determine_child_bins(bins_cluster,P_different, messages_count, gap_vector,0)

chi_different_frequencies = anomalous_bins_frequencies(M_T, chi_different_bins)
unique_templates_anomalous, rare_templates_anomalous = analyze_bins_and_write(chi_different_frequencies, chi_different_bins, Templates_stats, rare_threshold,"different")

#----------------------------------------------------------------------#
# Messages that the CHI tets was not able to tests
#----------------------------------------------------------------------#
chi_ineffective_indeces=find_overlapping_indeces_parents(flags,gap_vector,"ineffective",bins_cluster, parents_distribution)#find_overlapping_indeces_new(flags,gap_vector,"ineffective")
chi_ineffective_bins, P_ineffective = determine_anomalous_bins_parents(chi_ineffective_indeces,parents_distribution,"ineffective")
pops_with_threshold(chi_ineffective_bins,P_ineffective,10000)
ineffective_child_bins, bad_parents_of_ineffective_child = determine_child_bins(bins_cluster,P_ineffective, messages_count, gap_vector,0)# determine_child_bins(bins_cluster,P, messages_count, gap_vector)


chi_ineffective_frequencies = anomalous_bins_frequencies(M_T,chi_ineffective_bins)
unique_templates_ineffective_chi, rare_templates_ineffective_chi = analyze_bins_and_write(chi_ineffective_frequencies, chi_ineffective_bins, Templates_stats, rare_threshold, "ineffective")


#------------------------------------------------------------------------------#
# Write a txt file with all the templates
#------------------------------------------------------------------------------#
write_templates(templates)

#------------------------------------------------------------------------------#
# Write txt files with anomalous bins of messages
#------------------------------------------------------------------------------#
# write parents bins
write_different_distribution_messages(address,chi_different_indeces)
write_chi_ineffective_messages(address,chi_ineffective_indeces)

# write unique or rare lines
write_lines(address,[unique_templates_ineffective_chi, rare_templates_ineffective_chi])

# write child bins
write_vector_of_interval_of_messages(address, different_child_bins, "different")
write_vector_of_interval_of_messages(address, ineffective_child_bins, "ineffective") 
#------------------------------------------------------------------------------#

#>>> tt=generate_templates(60, 20)
#>>> c,a,b=generate_syslog_with_anomalies(100000, tt,15,15 )


A=compare(c["type"],different_child_bins)

B,groups_detected=compare(c["type"],ineffective_child_bins + different_child_bins)
print(B)
print(groups_detected)
print(artificial_group_anomaly)
print(ineffective_child_bins + different_child_bins)

#------------------------------------------------------------------------------#
# Visualization of the results: creating dataset for D3.js
#------------------------------------------------------------------------------#
#   --- Bubbles: --- 

#   - Templates: -
# Create list: [[index, occurrences_of_template, words_of_template], ...]
index_templatesOcc_words = template_occurrences(Templates_stats)
headers = ["index","value","words"]
# Write a json file from this list for the bubble visualization tool.
write_json_from_list(index_templatesOcc_words,headers,"index_templates",["N","N","S"])

#   - Distributions: -
# Create dictionary: distributions_occurrences{['gap_type'], ['distributions_index'], ['distributions_occurrences'] }
distributions_occurrences=distributions_occurrences(bins_cluster, distributions, gap_vector)
# Write a json file from this dictionary for the bubble visualization tool 
write_json_from_dictionary(distributions_occurrences,"distributions",["S","N","N"])



#   --- Forces: ---

#   - Templates: -
# Create dictionary: T{["t0"], ["t1"], ...} 
# each element contains a vector with values indicating what templates follow the selected one in the following number of messages (slots_T_around) 
slots_T_around = 5
T=templates_around(slots_T_around,M_T,templates)
# Write a json file from this dictionary for the force visualization tool
write_force_json_from_dictionary(T,index_templatesOcc_words,"templates")


#   - Distributions: -
slots_D_around = 5
D = distributions_around(slots_D_around,distributions,bins_cluster,[gap_vector[0]])
index_distributionOcc_frequencies = index_distributionOcc_freq(distributions_occurrences,distributions,gap_vector)
write_force_json_from_dictionary_dist(D,index_distributionOcc_frequencies["gap_"+str(gap_vector[0])],"distributions"+str(gap_vector[0]),[gap_vector[0]])



print("\n json dataset ready for D3.js! \n")

#------------------------------------------------------------------------------#
# Compute elapsed time
#------------------------------------------------------------------------------#
elapsed = time.time() - t
print("Elapsed time: {0}".format(elapsed))
        