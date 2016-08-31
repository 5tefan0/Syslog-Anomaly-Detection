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
                if index_V == len(vector_of_interval_of_messages) -1:
                    break
                index_V += 1
                still_writing = False
                intervals= vector_of_interval_of_messages[index_V]
                g.write(" \n\n\n ----------\n\n\n".format(files))
                continue
            else:
                assert(False)
            C+=1
    g.close()
    print("\n Done!  \n\n")
