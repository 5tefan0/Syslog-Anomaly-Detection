#------------------------------------------------------------------------------#
# Creates a dictionary with statistics concerning the distributions:
#------------------------------------------------------------------------------#
def distributions_occurrences(bins_cluster, distributions, gap_vector):
    D = {}
    total_length=0
    for gap in gap_vector:
        total_length += len(distributions["gap_"+str(gap)])
    D["distributions_occurrences"] = [0]*total_length
    D["gap_type"] = [" "]*total_length
    D["distributions_index"] = [0]*total_length
    for i in range(total_length):
        if i==0:
            continue
        D["distributions_index"][i]=D["distributions_index"][i-1]+1
    for gap in gap_vector:
        for b in bins_cluster["gap_"+str(gap)]:
            D["distributions_occurrences"][b] +=1
            D["gap_type"][b] = str(gap)
    return D


def index_distributionOcc_freq(distributions_occurrences,distributions,gap_vector):
    output={}
    l=0
    for gap in gap_vector:
        output["gap_"+str(gap)]=[]
        for d in distributions_occurrences['distributions_index']:
            if distributions_occurrences['gap_type'][d]==str(gap):
                index=d
                occurences=distributions_occurrences['distributions_occurrences'][d]
                freq=make_string_from_distr(distributions["gap_"+str(gap)][d-l])#str(distributions["gap_"+str(gap)][d-l])
                output["gap_"+str(gap)].append([index,occurences,freq])
            else:
                continue
        l=len(distributions["gap_"+str(gap)]) # to get the right index in distributions["gap_"+str(gap)]
    return output

def make_string_from_distr(d):
    new=" "
    for i in d:
        new+= str(i) + " - "
    return new




#------------------------------------------------------------------------------#
# Creates a json file:
# Input: dictionary, file_name, input_type vector ("N" for number, "S" for string)
#------------------------------------------------------------------------------#
def write_json_from_dictionary(dictionary,file_name,input_type):
    headers = list(dict.keys(dictionary))
    g = open(file_name+".json","w")
    g.write("[\n")
    for i in range(len(dictionary[headers[0]])):
        g.write("{ \n")
        for x in range(len(headers)):
            if x < len(headers)-1:
                if input_type[x] == "S":
                    g.write(' "{0}": "{1}",\n'.format(headers[x],dictionary[headers[x]][i]))
                elif input_type[x] == "N":
                    g.write(' "{0}": {1},\n'.format(headers[x],dictionary[headers[x]][i]))
                else:
                    assert(False)
            else: # you don't need a comma after last category
                if input_type[x] == "S":
                    g.write(' "{0}": "{1}"\n'.format(headers[x],dictionary[headers[x]][i]))
                elif input_type[x] == "N":
                    g.write(' "{0}": {1}\n'.format(headers[x],dictionary[headers[x]][i]))
                else:
                    assert(False)
        if i < len(dictionary[headers[0]])-1:
            g.write("},\n")
        else: # you don't need a comma after last entry
            g.write("}\n")
    g.write("]")

#------------------------------------------------------------------------------#
# finds distributions around a distribution (next slots)
#------------------------------------------------------------------------------#

def distributions_around(slots,distributions,bins_cluster,gap_vector):
    D_around = {}
    g_before=0
    len_before=0
    for g in gap_vector:
        for i in range(g_before,g_before+len(distributions["gap_"+str(g)])):
            D_around["gap_"+str(g)+"_d"+str(i)]=[0]*(len(distributions["gap_"+str(g)])+len_before)
        for d in range(len(bins_cluster["gap_"+str(g)])-slots-1):
            force = 1
            for y in bins_cluster["gap_"+str(g)][(d+1):(d+slots+1)]:
                D_around["gap_"+str(g)+"_d"+str(bins_cluster["gap_"+str(g)][d])][y] += 1/force
                force +=1
        g_before = len(distributions["gap_"+str(g)])
        len_before = len(distributions["gap_"+str(g)])
    return D_around

# def distributions_around_bins(slots,distributions,bins_cluster,g):
#     D_around = {}
#     for i in range(len(distributions)):
#         D_around["gap_"+str(g)+"_d"+str(i)]=[0]*len(distributions)
#     for d in range(len(bins_cluster)-slots-1):
#         force = 1
#         for y in bins_cluster[(d+1):(d+slots+1)]:
#             D_around["gap_"+str(g)+"_d"+str(bins_cluster[d])][y] += 1/force
#             force +=1
#     return D_around

#------------------------------------------------------------------------------#
# Force layout distributions
#------------------------------------------------------------------------------#
def write_force_json_from_dictionary_dist(D,i_d_f,file_name,gap_vector):
    headers = list(dict.keys(D))
    g = open(file_name+"_force.json","w")
    g.write("{\n")
    k = count_positive_entries(D[headers[-1]])
    # start nodes section
    g.write('"nodes": [\n')
    for t in range(len(headers)):
        if t < len(headers)-1:
            g.write("{")
            g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"name", i_d_f[t][1],"occurrences",i_d_f[t][2],"frequencies"))
            g.write("},\n")
        else: # you don't need a comma after last category
            g.write("{")
            g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"name", i_d_f[t][1],"occurrences",i_d_f[t][2],"frequencies"))
            g.write("}\n")
    g.write("],\n")
    # start edges section
    g.write('"links": [\n')
    for t in range(len(headers)):
        if t < len(headers)-1:
            for f in range(len(headers)):
                if D[headers[t]][f] > 0:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}"  '.format(headers[t],"source","gap_90_d"+str(f),"target",D[headers[t]][f],"value"))
                    g.write("},\n")
                else:
                     continue
        else:
            c = 0
            for f in range(len(headers)):
                if D[headers[t]][f] > 0 and c < k-1:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"source","gap_90_d"+str(f),"target",D[headers[t]][f],"value"))
                    g.write("},\n")
                    c += 1
                elif D[headers[t]][f] > 0 and c == k-1:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"source","gap_90_d"+str(f),"target",D[headers[t]][f],"value"))
                    g.write("}\n")
                else:
                    continue
    g.write("]\n")
    g.write("}")


def count_positive_entries(t):
    c=0
    for i in range(len(t)):
        if t[i]>0:
            c+=1
    return c
