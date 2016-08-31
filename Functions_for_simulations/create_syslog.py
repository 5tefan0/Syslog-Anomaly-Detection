#------------------------------------------------------------------------------#
# Creates a fake sislog file
#------------------------------------------------------------------------------#

import random
import string
import numpy as np

#from itertools import islice

# random.choice(string.ascii_lowercase)  random.choice(string.ascii_uppercase)  random.choice(string.ascii_letters)

#------------------------------------------------------------------------------#
# Create templates
#------------------------------------------------------------------------------#
def generate_templates(number_of_templates, mean_template_length):
    templates = {}
    templates["words"]=[]
    templates["words_type"]=[]
    templates["words_length"]=[]
    templates["template_length"]=[]
    for i in range(number_of_templates):
        words_type = []
        words_length = []
        words = []
        length = np.random.poisson(mean_template_length, 1)[0] #length of template i
        for word in range(length):
            if word < 1:
                words_type.append(0)
                words_length.append(4)
                add_word(words_length[-1],words_type[-1],words)
            else:
                if words_type[-1] == 0: # you had a parameter
                    words_type.append(np.random.binomial(1,0.90)) # if you had a parameter it is more likely to get a key word
                    words_length.append(np.random.poisson(9, 1)[0]) # random length of the (likely) key word
                    add_word(words_length[-1],words_type[-1],words)
                else:
                    words_type.append(np.random.binomial(1,0.55)) # if you had a key word it is more likely to get a parameter
                    words_length.append(np.random.poisson(11, 1)[0]) # random length of the (likely) parameter
                    add_word(words_length[-1],words_type[-1],words)
        templates["words"].append(words)
        templates["words_type"].append(words_type)
        templates["words_length"].append(words_length)
        templates["template_length"].append(length)
    write_templates2(templates)
    return templates

def add_word(W_size,W_type,vector):
    W = ""
    if W_type == 0: # type 0 means it's a parameter
            W += "*" #random.choice(string.ascii_lowercase)
    else: # type 1 means it's a key word
        for i in range(W_size):
            W += random.choice(string.ascii_uppercase)
    return vector.append(W)


def write_templates2(templates):
    g = open("generated_templates.txt","w")
    for i in range(len(templates["words"])):
        g.write("{0}\n".format(templates["words"][i]))
    g.close()

#------------------------------------------------------------------------------#
# Create file from templates
#------------------------------------------------------------------------------#

# np.random.multinomial(20, [1/6.]*6, size=1)
"""
def generate_syslog(number_of_lines, templates, number_of_anomalies):
    g = open("generated_syslog.txt","w")
    logs={}
    logs["lines"]=[]
    logs["type"]=[]
    anomalies_count = 0
    P = probabilities_of_templates(templates)
    for i in range(number_of_lines):
        logs["type"].append(np.random.binomial(1,0.95)) #with p 0.95 it's a normal line
        if logs["type"][-1]==1: # add normality
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
        elif logs["type"][-1]==0 and anomalies_count < number_of_anomalies:
            new_anomaly = True
            skips =0
            skips = add_anomaly(skips,new_anomaly,g,logs["lines"],15)  ### !!!!!!!!
            anomalies_count+=1
            i += skips
        else: # we reached the maximum number of anomalies so we are adding a normality
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
    g.close()
    return logs

def generate_syslog_two_types_of_anomaly(number_of_lines, templates, number_of_anomalies_single, number_of_anomalies_group ):
    g = open("generated_syslog_two.txt","w")
    logs={}
    logs["lines"]=[]
    logs["type"]=[]
    anomalies_count_single = 0
    anomalies_count_group = 0
    P = probabilities_of_templates2(templates) ###
    for i in range(number_of_lines):
        logs["type"].append(np.random.binomial(1,0.95)) #with p 0.95 it's a normal line
        if logs["type"][-1]==1: # add normality
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
        elif logs["type"][-1]==0 and anomalies_count_single + anomalies_count_group < number_of_anomalies_single + number_of_anomalies_group:
            new_anomaly = True
            anomaly_type = np.random.binomial(1,0.4) #1 for single anomaly , 0 for group
            if anomaly_type == 1:
                skips =0
                skips = add_anomaly(skips,new_anomaly,g,logs["lines"],15)  ### !!!!!!!!
                anomalies_count_single+=1
                i += skips
            else: # add group with different probs
                for j in range(100):
                    template_to_use_vector = np.random.multinomial(1, reverse_probabilities2(P), size=1)[0]
                    k = template_index(template_to_use_vector)
                    new_line=add_normality(g,templates,k)
                    logs["lines"].append(new_line)
                anomalies_count_group+=1
        else: # we reached the maximum number of anomalies so we are adding a normality
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
    g.close()
    return logs
"""
def template_index(template_to_use_vector):
    k=0
    for k in range(len(template_to_use_vector)): #get index of the template
        if template_to_use_vector[k] == 1:
            return k
    assert(False)

def probabilities_of_templates(templates):
    p = []
    for i in range(len(templates["words"])):
        p.append(1/len(templates["words"]))
    p[0]+=2*(1/len(templates["words"]))
    p[1]+=1*(1/len(templates["words"]))
    p[2]+=1*(1/len(templates["words"]))
    p[-1] -= 0.8*(1/len(templates["words"]))
    p[-2] -= 0.8*(1/len(templates["words"]))
    p[-3] -= 0.8*(1/len(templates["words"]))
    p[-4] -= 0.8*(1/len(templates["words"]))
    p[-5] -= 0.8*(1/len(templates["words"]))
    return p

def probabilities_of_templates3(templates):
    new_p=[]
    for i in range(len(templates["words"])):
        if i >= 0 and i < 5:
            new_p.append(0.20)
        else:
            new_p.append(0)
    return new_p

def reverse_probabilities(p):
    new_p=[]
    for i in range(len(p)):
        new_p.append(p[-(i+1)])
    return new_p

def reverse_probabilities2(p):
    new_p=[]
    for i in range(len(p)):
        if i >= 10 and i < 15:
            new_p.append(0.20)
        else:
            new_p.append(0)
    return new_p

def probabilities_of_templates2(templates):
    p = []
    for i in range(len(templates["words"])):
        if i>=0 and i< 10:
            p.append(0.1)
        else:
            p.append(0)
    return p

def add_anomaly(skips,new_anomaly,file_to_write,vector,mean_length):
    if new_anomaly == True:
        skips = 0
    anomaly = ""
    anomaly_length = np.random.poisson(mean_length, 1)[0]
    for i in range(anomaly_length):
        W=""
        for i in range(np.random.poisson(mean_length - 4, 1)[0]):
            W += random.choice(string.ascii_letters)
        anomaly += W + " "
    file_to_write.write("{0} \n".format(anomaly))
    vector.append(anomaly)
    add_another = np.random.binomial(1,0.75)
    if add_another == 1:
        new_anomaly = False
        add_anomaly(skips,new_anomaly,file_to_write,vector,mean_length)
        skips+=1
    else:
        new_anomaly=True
    return skips

def add_normality(file_to_write,vector,template_index):
    new_line = ""
    W=""
    for words in vector["words"][template_index]:
        if words == "*":
            parameter_length = 1# np.random.poisson(9, 1)[0]
            for i in range(parameter_length):
                W += "p"#random.choice(string.ascii_lowercase)
            new_line += W + " "
            W =""
            continue
        else:
            new_line += words + " "
    file_to_write.write("{0} \n".format(new_line))
    return new_line

#last version:
def generate_syslog_with_anomalies(number_of_lines, templates, number_of_anomalies_single, number_of_anomalies_group ):
    g = open("generated_syslog_with_anomalies.txt","w")
    anomalous_different_bins = []
    logs={}
    logs["lines"]=[]
    logs["type"]=[]
    anomalies_count_single = 0
    anomalies_count_group = 0
    skips=0
    P = probabilities_of_templates3(templates) ###############
    n_of_lines = iter(range(number_of_lines))
    for i in n_of_lines:
        if i < 10000: # add normality
            logs["type"].append(1)
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
            continue
        if skips >0:
            skips -= 1
            continue
        logs["type"].append(np.random.binomial(1,0.9999)) #with p 0.95 it's a normal line
        if logs["type"][-1]==1: # add normality
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
        elif logs["type"][-1]==0 and (anomalies_count_single < number_of_anomalies_single or  anomalies_count_group < number_of_anomalies_group):
            if anomalies_count_single < number_of_anomalies_single and anomalies_count_group < number_of_anomalies_group:
                q=0.5
            elif anomalies_count_single >= number_of_anomalies_single:
                q=0
            else:
                q=1
            new_anomaly = True
            anomaly_type = np.random.binomial(1,q) #1 for single anomaly , 0 for group
            if anomaly_type == 1:
                skips =0
                skips = add_anomaly2(skips,new_anomaly,g,logs["lines"],logs["type"],15)  ### !!!!!!!!
                anomalies_count_single+=1
            else: # add group with different probs
                skips = 69
                anomalous_different_bins.append([i,i+skips])
                for j in range(skips+1):
                    logs["type"][-1]=2
                    template_to_use_vector = np.random.multinomial(1, reverse_probabilities2(P), size=1)[0]
                    k = template_index(template_to_use_vector)
                    new_line=add_normality_anomaly(g,templates,k)
                    logs["lines"].append(new_line)
                    if j > 0:
                        logs["type"].append(2)
                anomalies_count_group+=1
                i += skips
        else: # we reached the maximum number of anomalies so we are adding a normality
            logs["type"][-1]=1
            template_to_use_vector = np.random.multinomial(1, P, size=1)[0]
            k = template_index(template_to_use_vector)
            new_line=add_normality(g,templates,k)
            logs["lines"].append(new_line)
    g.close()
    return logs, anomalies_count_single, anomalies_count_group, anomalous_different_bins



def add_normality_anomaly(file_to_write,vector,template_index):
    new_line = ""
    W=""
    for words in vector["words"][template_index]:
        if words == "*":
            parameter_length = np.random.poisson(9, 1)[0]
            for i in range(parameter_length):
                W += "Y"#random.choice(string.ascii_lowercase)
            new_line += W + " "
            W =""
            continue
        else:
            new_line += words + " "
    file_to_write.write("{0} \n".format(new_line))
    return new_line

# this type of anomaly is just a random template
def add_anomaly2(skips,new_anomaly,file_to_write,vector, types,mean_length):
    if new_anomaly == True:
        skips = 0
    anomaly = ""
    anomaly_length = np.random.poisson(mean_length, 1)[0]
    for i in range(anomaly_length):
        W=""
        for i in range(np.random.poisson(mean_length - 4, 1)[0]):
            W += "X"#random.choice(string.ascii_letters)
        anomaly += W + " "
    file_to_write.write("{0} \n".format(anomaly))
    vector.append(anomaly)
    another_prob = 0.9
    add_another = np.random.binomial(1,another_prob)
    while add_another > 0:
        #print("adding another")
        types.append(0)
        new_anomaly = False
        skips+=1
        #print(skips)
        anomaly = ""
        anomaly_length = np.random.poisson(mean_length, 1)[0]
        for i in range(anomaly_length):
            W=""
            for i in range(np.random.poisson(mean_length - 4, 1)[0]):
                W += "X"#random.choice(string.ascii_letters)
            anomaly += W + " "
        file_to_write.write("{0} \n".format(anomaly))
        vector.append(anomaly)
        another_prob -= 0.1
        add_another = np.random.binomial(1,max(0,another_prob))
        #add_anomaly2(skips,new_anomaly,file_to_write,vector,types,mean_length)
    else:
        new_anomaly=True
    return skips
