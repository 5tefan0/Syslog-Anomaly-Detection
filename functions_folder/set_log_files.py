#------------------------------------------------------------------------------#
# Set the list of the log files to analize
#------------------------------------------------------------------------------#
def set_log_files(cloud,file_type,Y):
    address =[]
    if file_type == "simulation":
        address.append("/Users/Stefano/Dropbox (MIT)/IIJ/templateminer/templateminer/generated_syslog_with_anomalies.txt")
        #address.append("/Volumes/UNTITLED/generated_syslog_with_anomalies.log")
        #address.append("/templateminer/generated_syslog_with_anomalies.log")
        #address.append("/UNTITLED/generated_syslog_with_anomalies.log")/Dropbox\ \(MIT\)
        return address
    months_in_2015 = ["08","09","10","11","12"]
    months_in_2016 = ["01","02","03","04","05","06"]
    if file_type == "nat": # nat.log has files only until December 2nd 2015
        Y = ["2015"]
        months_in_2015 = ["08","09","10","11"]
    if cloud == "wide":
        months_in_2015 = ["10","11"]
    for year in Y:
        if year == "2015":
            for month in months_in_2015:
                if month in ["08", "10", "12"]:
                    for p in range(1,32): # days from 1 to 31
                        if p<10:
                            date = year + month + "0"+str(p)
                        else:
                            date = year + month +str(p)
                        address.append("/Volumes/UNTITLED/"+cloud+"-cloud/"+date+"/"+file_type+".log")
                else:
                    for p in range(1,31): # days from 1 to 30
                        if p<10:
                            date = year + month + "0"+str(p)
                        else:
                            date = year + month +str(p)
                        address.append("/Volumes/UNTITLED/"+cloud+"-cloud/"+date+"/"+file_type+".log")
        if year == "2016":
            for month in months_in_2016:
                if month == "02":
                    for p in range(1,29): # only from 1 to 28 for February
                        if p<10:
                            date = year + month+"0"+str(p)
                        else:
                            date = year + month +str(p)
                        address.append("/Volumes/UNTITLED/"+cloud+"-cloud/"+date+"/"+file_type+".log")
                elif month in ["01","03","05"]:
                    for p in range(1,32): # days from 1 to 31
                        if p<10:
                            date = year + month+"0"+str(p)
                        else:
                            date = year + month +str(p)
                        address.append("/Volumes/UNTITLED/"+cloud+"-cloud/"+date+"/"+file_type+".log")
                else:
                    for p in range(1,31): # days from 1 to 30
                        if p<10:
                            date = year + month+"0"+str(p)
                        else:
                            date = year + month +str(p)
                        address.append("/Volumes/UNTITLED/"+cloud+"-cloud/"+date+"/"+file_type+".log")
    print("Log files set.")
    return address

#------------------------------------------------------------------------------#
