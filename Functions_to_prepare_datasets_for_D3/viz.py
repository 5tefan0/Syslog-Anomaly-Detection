
# visualize templates

import numpy as np

# export templates occurrences vector

def template_occurrences(Templates_stats):
    vector=[]
    for i in range(len(Templates_stats)):
        vector.append([i,Templates_stats[i]._counts,Templates_stats[i]._words])
    #numpy.savetxt("template_occurrences.csv", vector, delimiter=",", header='template_index, occurrences', fmt='%d')
    return vector
    #return vector







#------------------------------------------------------------------------------#
# Creates a json file:
# Input: list, list of headers for the entries, file name and input_type vector ("N" for number, "S" for string)
# list: index, occurences, template
#------------------------------------------------------------------------------#
def write_json_from_list(list,headers,file_name,input_type):
    g = open(file_name+".json","w")
    g.write("[\n")
    for i in range(len(list)):
        g.write("{ \n")
        for x in range(len(list[0])):
            if x < len(list[0])-1:
                v = list[i][x]
                if input_type[x] == "S":
                    g.write(' "{0}": "{1}",\n'.format(headers[x],list[i][x]))
                elif input_type[x] == "N":
                    g.write(' "{0}": {1},\n'.format(headers[x],list[i][x]))
                else:
                    assert(False)
            else: # you don't need a comma after last category
                if input_type[x] == "S":
                    g.write(' "{0}": "{1}"\n'.format(headers[x],list[i][x]))
                elif input_type[x] == "N":
                    g.write(' "{0}": {1}\n'.format(headers[x],list[i][x]))
                else:
                    assert(False)
        if i < len(list)-1:
            g.write("},\n")
        else: # you don't need a comma after last entry
            g.write("}\n")
    g.write("]")


#------------------------------------------------------------------------------#
# finds templates around a template (next slots)
#------------------------------------------------------------------------------#

def templates_around(slots,M_T,templates):
    T_around = {}
    for i in range(len(templates)):
        T_around["t"+str(i)]=[0]*len(templates)
    for m in range(len(M_T)-slots-1):
        force = 1
        for y in M_T[(m+1):(m+slots+1)]:
            T_around["t"+str(M_T[m])][M_T[y]] += 1/force
            force +=1
    return T_around


#------------------------------------------------------------------------------#
# Force layout template
#------------------------------------------------------------------------------#
def write_force_json_from_dictionary(T,index_templates_words,file_name):
    headers = list(dict.keys(T))
    g = open(file_name+"_force.json","w")
    g.write("{\n")
    k = count_positive_entries(T[headers[-1]])
    # start nodes section
    g.write('"nodes": [\n')
    for t in range(len(headers)):
        if t < len(headers)-1:
            g.write("{")
            g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"name", index_templates_words[int(headers[t][1:])][1],"occurrences",index_templates_words[int(headers[t][1:])][2],"words"))
            g.write("},\n")
        else: # you don't need a comma after last category
            g.write("{")
            g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"name", index_templates_words[int(headers[t][1:])][1],"occurrences",index_templates_words[int(headers[t][1:])][2],"words"))
            g.write("}\n")
    g.write("],\n")
    # start edges section
    g.write('"links": [\n')
    for t in range(len(headers)):
        if t < len(headers)-1:
            for f in range(len(headers)):
                if T[headers[t]][f] > 0:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}"  '.format(headers[t],"source","t"+str(f),"target",T[headers[t]][f],"value"))
                    g.write("},\n")
                else:
                    continue
        else:
            c = 0
            for f in range(len(headers)):
                if T[headers[t]][f] > 0 and c < k-1:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"source","t"+str(f),"target",T[headers[t]][f],"value"))
                    g.write("},\n")
                    c += 1
                elif T[headers[t]][f] > 0 and c == k-1:
                    g.write("{")
                    g.write(' "{1}": "{0}", "{3}": "{2}", "{5}": "{4}" '.format(headers[t],"source","t"+str(f),"target",T[headers[t]][f],"value"))
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
