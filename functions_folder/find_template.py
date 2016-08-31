from classes_setup import Template

def find_template(i,new_message,comparing_template,templates,Templates_stats):
    new_template=[]
    same_key_words=0
    stars=0
    has_stars=False
    for j in  range(len(new_message)):
            if comparing_template[j]==new_message[j]:
                new_template.append(comparing_template[j])
                same_key_words+=1
                continue
            if comparing_template[j]=="*": #if template has a star keep the star but do not increase count
                new_template.append("*")
                has_stars = True
                continue
                #stars += 1
            if comparing_template[j]!=new_message[j]:
                new_template.append("*")
                stars+=1
    if stars > same_key_words +1 and has_stars:
        #print("too many stars")
        FoundMatching = False
    elif stars > same_key_words + 4:
        FoundMatching = False
    else: # You found a match! So update the old template (maybe you found new parameters)
        templates[i]=new_template #update template stats
        Templates_stats[i]._words=templates[i]
        FoundMatching = True
        #print("{0} turn, match found".format(i))
    return(FoundMatching)

def template_vector_to_string(vector_of_string):
    result = " "
    vector_of_string_wo_quotes = delete_quotes(vector_of_string)
    for i in range(len(vector_of_string_wo_quotes)):
        if vector_of_string_wo_quotes[i]=='"${rc}':
            result += "${rc}" + " "
            continue
        result += vector_of_string_wo_quotes[i]+ " "
    return result

def delete_quotes(vector_of_string):
    new_vector_of_string=[]
    for w in vector_of_string:
        new_word=""
        for sign in w:
            if sign == '"':
                continue
            else:
                new_word += sign
        new_vector_of_string.append(new_word)
    return new_vector_of_string
