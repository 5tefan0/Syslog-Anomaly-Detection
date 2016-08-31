#from tqdm import tqdm
#------------------------------------------------------------------------------#
# Write the templates in "TemplatesFound.txt"
#------------------------------------------------------------------------------#
def write_templates(templates):
    print("Writing Templates")
    g = open("TemplatesFound.txt","w")
    for k in range(len(templates)):
        g.write("{0} \n".format(templates[k]))
    g.close()
    print("\n Done! \n\n")

#------------------------------------------------------------------------------#
# Write messages in "different_distribution_messages.txt" that are in bins of different distribution
#------------------------------------------------------------------------------#
def write_different_distribution_messages(address,INDICES):
    print(" Writing different distribution messages ... ")
    NonAncora=True
    g = open("chi_different_messages.txt","w")
    if len(INDICES) == 0:
        print("\n Nothing to write")
        g.close()
        return
    C=0
    still_writing = False
    for files in address:
        f = open(files,"r")
        g.write(" \n\n\n ----- FILE: {0} -----\n\n\n".format(files))
        for line in f:
            C+=1
            if C < INDICES[0]:
                continue
            elif C in INDICES:
                if still_writing:
                    g.write("{0} \n".format(line))
                    still_writing = True
                else:
                    g.write(" \n\n\n -------- NEW ANOMALY --------\n\n\n".format(files))
                    g.write("{0} \n".format(line))
                    still_writing = True
            elif C > INDICES[-1]:
                break
            else:
                still_writing = False
                continue
    g.close()
    print("\n Done! {0} different distribution messages found.  \n\n".format(len(INDICES)))

#------------------------------------------------------------------------------#
# Write messages in "chi_ineffective_messages.txt that are in bins that the Chi Square tests was not able to analyze, probably because of some rare event
#------------------------------------------------------------------------------#
def write_chi_ineffective_messages(address,INDICES):
    print(" Writing chi ineffective messages ... ")
    g = open("chi_ineffective_messages.txt","w")
    if len(INDICES) == 0:
        print("\n Nothing to write")
        g.close()
        return
    NonAncora=True
    C=0
    still_writing = False
    for files in address:
        f = open(files,"r")
        g.write(" \n\n\n ----- FILE: {0} -----\n\n\n".format(files))
        for line in f:
            C+=1
            if C < INDICES[0]:
                continue
            elif C in INDICES:
                if still_writing:
                    g.write("{0} \n".format(line))
                    still_writing = True
                else:
                    g.write(" \n\n\n -------- NEW ANOMALY --------\n\n\n".format(files))
                    g.write("{0} \n".format(line))
                    still_writing = True
            elif C > INDICES[-1]:
                break
            else:
                still_writing = False
                continue
    g.close()
    print("\n Done! {0} chi ineffective messages found. \n\n".format(len(INDICES)))

#------------------------------------------------------------------------------#
# Write anomalous lines
#------------------------------------------------------------------------------#
def write_lines(address, vector_of_vectors_of_messages):
    print(" Writing lines ... ")
    g = open("strange_lines.txt","w")
    if len(vector_of_vectors_of_messages) == 0:
        print("\n Nothing to write")
        g.close()
        return
    for INDICES in vector_of_vectors_of_messages:
        if len(INDICES) == 0:
            continue
        g.write("\n\n +++++++++++++++++++++++++++ \n\n")
        C=0
        still_writing = False
        for files in address:
            still_writing == False  #?
            f = open(files,"r")
            for line in f:
                C+=1
                if C < INDICES[0]:
                    continue
                elif C in INDICES:
                    if still_writing == False :
                        g.write(" \n\n\n ----- FILE: {0}, line: {1} -----\n\n\n".format(files, C))
                    g.write("{0} \n".format(line))
                elif C > INDICES[-1]:
                    break
                else:
                    still_writing = False
                    continue
    g.close()
    print("\n Done!  \n\n")

#------------------------------------------------------------------------------#
# Write child bins
#------------------------------------------------------------------------------#
def write_vector_of_interval_of_messages(address, vector_of_interval_of_messages, chi_result): #vector of vectors of intervals
    print(" Writing child bins ... ")
    g = open("child_"+chi_result+"_bins.txt","w")
    if len(vector_of_interval_of_messages) == 0:
        print("\n Nothing to write")
        g.write("\n Nothing to write")
        g.close()
        return
    index_V=0
    intervals= vector_of_interval_of_messages[index_V]
    files_used=0
    C=0
    still_writing = False
    for files in address:
        change_file = False
        files_used += 1
        f = open(files,"r")
        for line in f:
            if change_file:
                break
            C+=1
            if C < intervals[0]:
                continue
            elif C >= intervals[0] and C <= intervals[1]:
                if still_writing == False :
                    g.write("\n\n ++++++++++++ new child interval for messages in [{0},{1}]+++++++++++++++ \n\n".format(intervals[0],intervals[1]))
                    g.write(" \n\n\n ----- FILE: {0} -----\n\n\n".format(files))
                    still_writing = True
                g.write("{0} \n".format(line))
                continue
            elif C > intervals[1]:
                index_V += 1
                still_writing = False
                intervals= vector_of_interval_of_messages[index_V]
                break
            else:
                assert(False)
            C+=1
    g.close()
    print("\n Done!  \n\n")
