#------------------------------------------------------------------------------#
# Analyze anomalous bins
#------------------------------------------------------------------------------#

from classes_setup import Template

def analyze_bins(bins_vector, Templates_stats, rare_threshold):
    unique_templates = []
    rare_templates = []
    print("\n Analyzing bins: \n")
    bins_count = 0
    for bin in bins_vector:
        bins_count += 1
        Nothing_Strange = True
        print("\n Analyzing bin number {0}\n".format(bins_count))
        for t_f in bin:
            if t_f[1] == 1: # if template t_f appears only once
                template_index = t_f[0] # get the template index
                if Templates_stats[template_index]._counts == 1: # then this is the only time this particular template appears
                    print("\n Template " + str(template_index) + " appears only once.\n")
                    unique_templates.append(template_index)
                    Nothing_Strange = False
                    continue
                elif Templates_stats[template_index]._counts < rare_threshold:
                    print("\n Template " + str(template_index) + " is rare. It appears only {0} times in total, and only once in this bin.\n".format(Templates_stats[template_index]._counts))
                    rare_templates.append(template_index)
                    Nothing_Strange = False
                    continue
                else:
                    print("\n Template " + str(template_index) + " is not rare (it appears {0} times in total) but appears only once in this bin.\n".format(Templates_stats[template_index]._counts))
            elif t_f[1] < rare_threshold and Templates_stats[t_f[0]]._counts < rare_threshold:
                print("\n Template " + str(t_f[0]) + " is rare. It appears only {0} times in total, and only {1} in this bin.\n".format(Templates_stats[template_index]._counts , t_f[1]))
                Nothing_Strange = False
                continue
            else:
                continue
        if Nothing_Strange:
            print("Bin {0} has different templates appearing from other bins but the templates are not extremely rare\n".format(bins_count))
    return unique_templates, rare_templates


#bins_type either anomalous or chi_ineffective
def analyze_bins_and_write(bins_vector, bins_interval, Templates_stats, rare_threshold, bins_type):
    g = open("chi_"+bins_type+"_bins.txt","w")
    unique_templates = []
    rare_templates = []
    bins_count = 0
    for bin in bins_vector:
        Nothing_Strange = True
        g.write("\n Analyzing bin number {0}\n. Messages from {1} to {2}\n".format(bins_count, bins_interval[bins_count][0], bins_interval[bins_count][1]))
        for t_f in bin:
            if t_f[1] == 1: # if template t_f appears only once
                template_index = t_f[0] # get the template index
                if Templates_stats[template_index]._counts == 1: # then this is the only time this particular template appears
                    g.write("\n Template " + str(template_index) + " appears only once.\n")
                    unique_templates.append(template_index)
                    Nothing_Strange = False
                    continue
                elif Templates_stats[template_index]._counts < rare_threshold:
                    g.write("\n Template " + str(template_index) + " is rare. It appears only {0} times in total, and only once in this bin.\n".format(Templates_stats[t_f[0]]._counts))
                    rare_templates.append(template_index)
                    Nothing_Strange = False
                    continue
                else:
                    g.write("\n Template " + str(template_index) + " is not rare (it appears {0} times in total) but appears only once in this bin.\n".format(Templates_stats[t_f[0]]._counts))
            elif t_f[1] < rare_threshold and Templates_stats[t_f[0]]._counts < rare_threshold:
                g.write("\n Template " + str(t_f[0]) + " is rare. It appears only {0} times in total, and only {1} in this bin.\n".format(Templates_stats[t_f[0]]._counts , t_f[1]))
                Nothing_Strange = False
                continue
            else:
                continue
        if Nothing_Strange:
            g.write("\n Bin {0} has different templates appearing from other bins but the templates are not extremely rare\n".format(bins_count))
        bins_count += 1
    return unique_templates, rare_templates
