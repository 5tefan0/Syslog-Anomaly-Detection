#types: 1 normal , 0 new templates , 2 group different distribution

#pop first intervals?


def compare(types,bins):
    if bins == []:
        print("no bins\n")
        return
    results = {}
    results["normal_correct"] = 0
    results["normal_wrong"] = 0
    results["new_template_correct"] = 0
    results["new_template_wrong"] = 0
    results["new_group_correct"] = 0
    results["new_group_wrong"] = 0
    bins_number=len(bins)
    last_bin_mess = find_max_b(bins)
    new_group= False
    new_group_count = 0
    for index in range(len(types)):
        #print("##### index is {0} with type {1} #####\n".format(index,types[index]))
        if index > last_bin_mess:
            # message out of last bin
            if types[index] == 1:
                #print("it is a normal line")
                results["normal_correct"] += 1
                new_group = False
            elif types[index] == 0:
                #print("got a new template anomaly out of bin")
                results["new_template_wrong"] += 1
                new_group = False
            else: #2
                #print("got a new group anomaly out of bin")
                results["new_group_wrong"] += 1
                new_group = False
            continue
        for intervals in bins:
            #print("##### bin is {0} #####\n".format(intervals))
            a=intervals[0]
            b=intervals[1]
            bins_count=0
            if index > b:
                #assert(False)
                bins_count+=1
                if bins_count == bins_number:
                    out_of_last_bin = True
                else:
                    out_of_last_bin = False
                continue
            # message inside a bin:
            elif index >= a and index <= b:
                #print("index in bin")
                if types[index] == 1:
                    #print("it was a normal line")
                    results["normal_wrong"] += 1
                    new_group = False
                elif types[index] == 0:
                    results["new_template_correct"] += 1
                    new_group = False
                    #print("got a new template anomaly")
                else: #2
                    if new_group == False:
                        new_group = True
                        new_group_count +=1
                    results["new_group_correct"] += 1
                    #print("got a new group anomaly")
                break
            # message outiside the bin
            elif index < a:
                #print("index out of bin")
                if types[index] == 1:
                    #print("it is a normal line")
                    results["normal_correct"] += 1
                    new_group = False
                elif types[index] == 0:
                    #print("got a new template anomaly out of bin")
                    results["new_template_wrong"] += 1
                    new_group = False
                else: #2
                    #print("got a new group anomaly out of bin")
                    results["new_group_wrong"] += 1
                    new_group = False
                break
            else:
                assert(False)
    return results, new_group_count

# find max right extreme of the bins intervals
def find_max_b(bins):
    c=0
    for intervals in bins:
        #print("##### bin is {0} #####\n".format(intervals))
        a=intervals[0]
        b=intervals[1]
        c=max(0,c,b)
    return c

def pops_with_threshold(bins,P,threshold):
    if len(P)!=len(bins):
        print("Same size needed\n")
        assert(False)
    for intervals in bins:
        #print("##### bin is {0} #####\n".format(intervals))
        a=intervals[0]
        b=intervals[1]
        if b < threshold:
            P.pop(0)
