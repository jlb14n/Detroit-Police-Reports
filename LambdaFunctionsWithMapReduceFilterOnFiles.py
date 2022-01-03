import csv
from functools import reduce
import json
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Part 1: Model the Detroit Police Population
#Reading and cleaning the data
with open('911_Calls_for_Service_(Last_30_Days).csv','r') as file:
    csvreader= csv.reader(file)
    calls_as_dict = [{x:y for x,y in row.items()} for row in csv.DictReader(file)]
calls_as_dict_clean=list(filter(lambda x: x['zip_code']!='0' and x['neighborhood']!='', calls_as_dict))

#Total Response Time
total_response_times=list(filter(lambda x: x>=0, map(lambda x: float(x['totalresponsetime'] if x['totalresponsetime']!='' else -1), calls_as_dict_clean)))
avg_total_response_time=reduce(lambda x1,x2:x1+x2, total_response_times)/len(total_response_times)
print("The average response time is {0}".format(avg_total_response_time))

#Dispatch Time
dispatch_times=list(filter(lambda x: x>=0, map(lambda x: float(x['dispatchtime'] if x['dispatchtime']!='' else -1), calls_as_dict_clean)))
avg_dispatch_time=reduce(lambda x1,x2:x1+x2, dispatch_times)/len(dispatch_times)
print("The average dispatch time is {0}".format(avg_dispatch_time))

#Total Time
total_times=list(filter(lambda x: x>=0, map(lambda x: float(x['totaltime'] if x['totaltime']!='' else -1), calls_as_dict_clean)))
avg_total_time=reduce(lambda x1,x2:x1+x2, total_times)/len(total_times)
print("The average total time is {0}".format(avg_total_time))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Part 2: Model the Neighborhood Samples
#Divide list of dictionaries into smaller lists of dictionaries separated by neighborhood
neighborhoods=set()
[neighborhoods.add(x['neighborhood']) for x in calls_as_dict_clean]
calls_as_dict_organized=[list(filter(lambda x:x['neighborhood']==neighborhood,calls_as_dict_clean)) for neighborhood in sorted(neighborhoods)]

#Create a list of dictionaries for each neighborhood with average total response time, dispatch time, and total time
neighborhood_list=[]
for neighborhood in calls_as_dict_organized:
    #Initialize dictionary
    neighborhood_dict={}
    neighborhood_dict['Neighborhood']=neighborhood[0]['neighborhood']

    #Total Response Time
    total_response_times=list(filter(lambda x: x>=0, map(lambda x: float(x['totalresponsetime'] if x['totalresponsetime']!='' else -1), neighborhood)))
    neighborhood_dict['Average Total Response Time']=reduce(lambda x1,x2:x1+x2, total_response_times)/len(total_response_times)

    #Dispatch Time
    dispatch_times=list(filter(lambda x: x>=0, map(lambda x: float(x['dispatchtime'] if x['dispatchtime']!='' else -1), neighborhood))) 
    neighborhood_dict['Average Dispatch Time']=reduce(lambda x1,x2:x1+x2, dispatch_times)/len(dispatch_times)

    #Total Time
    total_times=list(filter(lambda x: x>=0, map(lambda x: float(x['totaltime'] if x['totaltime']!='' else -1), neighborhood)))   
    neighborhood_dict['Average Total Time']=reduce(lambda x1,x2:x1+x2, total_times)/len(total_times)

    #Append dictionary to list
    neighborhood_list.append(neighborhood_dict)
neighborhood_json=json.dumps(neighborhood_list, indent=4)
with open('911_Calls_for_Service_(Last_30_Days)_Neighborhood_Summary.json','w') as file:
    file.write(neighborhood_json)
