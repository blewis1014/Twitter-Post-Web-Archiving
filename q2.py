import os
import subprocess
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from datetime import date

timeMaps = []   # Holds TimeMaps for each URI
non_zero_data = []  # Holds TimeMaps for each URI with more than 0 mementos
tot_url_count = 0   # Total number of URIs
tot_mem_count = 0   # Total number of URIs with mementos

def collect_Timemaps():
    with open("testUrls.txt") as f:
        for line in f: 
            global tot_url_count
            print("#"+str(tot_url_count+1)+": Collecting from: " + line)
            result = subprocess.run(['memgator', '-f', 'JSON', '--hdrtimeout=1m30s', line], shell=True, capture_output=True)
            output = result.stdout
            global tot_mem_count
            
            if output == None or output == b'': # URI has no mementos and memgator call returns nothing
                memento_count = 0
                age_days = 0
                tot_url_count += 1
                print("Done")
            else:
                output_json = json.loads(output)    #Parses memgator output to a JSON object
                write_timeMaps_to_file(output_json)
                memento_count = count_mementos(output_json) 
                age_days = calculate_age(output_json)
                tot_url_count += 1
                tot_mem_count +=1
                print("Done")

            uri_dict = {"uri":line, "mementos": memento_count, "age":age_days}  #Dictionary for URIs
            if memento_count > 0:
                non_zero_data.append(uri_dict)
            else:
                timeMaps.append(uri_dict)




def write_timeMaps_to_file(output):
    outfile = open("timeMaps.txt","a")
    outfile.write(json.dumps(output, indent=2, sort_keys=True))
    outfile.close()

# Counts the number of mementos a link has
def count_mementos(output):
    mementos = len(output['mementos']['list'])
    return mementos

# Calculate the age of the first memento a link contains in days
def calculate_age(output):
    first_mem = output['mementos']['first']['datetime'] # 2020-10-01T03:07:29Z

    collection = datetime.date.today().strftime('%Y-%m-%d')
    datetime_coll = datetime.datetime.strptime(collection,'%Y-%m-%d')

    first_date = datetime.datetime.strptime(first_mem,'%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
    datetime_first = datetime.datetime.strptime(first_date,'%Y-%m-%d')

    age = datetime_coll - datetime_first
    return age.days

def print_timeMaps():
    global tot_url_count
    global tot_mem_count   
    for item in timeMaps:
        print(item)
        # tot_url_count+=1
    
    print("\nTotal Urls: "+str(tot_url_count))
    print("\nTotal Urls w/ Mementos: "+str(tot_mem_count))
        

def create_histogram():
    output_data = []
    for diction in timeMaps:
        output_data.append(diction['mementos'])

    non_zero_output = []
    for item in non_zero_data:
        non_zero_output.append(item['mementos'])

    range = (0,1000)
    bins = 20

    plt.hist(output_data,bins,range,color="red",histtype='bar', rwidth=0.8)
    plt.xlabel("# of Mementos")
    plt.ylabel("Frequency")
    plt.title("Q2: Total URIs")
    plt.show()
    plt.savefig('HistogramAll.png')

    # Excludes URIs with zero mementos
    plt.hist(non_zero_output,bins,range,color="blue",histtype='bar', rwidth=0.8)
    plt.xlabel("# of Mementos")
    plt.ylabel("Frequency")
    plt.title("Q2: Total URIs with > 0 mementos")
    plt.show()
    plt.savefig('HistogramNonZero.png')

def create_scatter():
    x = []
    y = []
    for diction in non_zero_data:
        x.append(diction['mementos'])
        y.append(diction['age'])

    plt.xlabel('# of mementos')
    plt.ylabel('Age in days')
    plt.title("Q3 Total URIs")
    plt.scatter(x,y, c="blue")
    plt.show()
    plt.savefig('Scatterplot.png')

if __name__ =='__main__':
    collect_Timemaps()
    create_histogram()
    create_scatter()
    print_timeMaps()
