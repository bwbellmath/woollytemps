# temps.py
import time
import csv
import os
import glob
from datetime import datetime

# prompt the user to name this experiment
ename = input("Enter Experiment Name: ")
print("Commencing Experiment: {}".format(ename))
# generate a .csv file for just this experiment
efile = "temps-{}.csv".format(ename)

# While true, with some time delay,
#   sleep(10) sleep for 1000ms -- we only want one reading per second or maybe a half second. 
#   read the temps from all sensors and
#     If all 3 sensors have been stable for a full minute, print "EQUILIBRIUM REACHED"
#       i.e. if all 3 sensors have max - min over the last n (5 minutes worth) values < epsilon = 1.0 degrees


base_dir = '/sys/bus/w1/devices'

# Identify the temperature sensors (map the addresses to names)
ds18b20s = {}
ds18b20s["ambient"] = "28-000008e3cca7"
ds18b20s["above"] ="28-00000d055acd"
ds18b20s["below"] ="28-00000d06287e"

#Store our device files to a list
device_files = []
device_files.append(base_dir + '/28-031197795ef3/w1_slave')
device_files.append(base_dir + '/28-e6a79d1964ff/w1_slave')
device_files.append(base_dir + '/28-61a79d1964ff/w1_slave')

def read_temp(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def get_temp(device_file):
    lines = read_temp(device_file)
    while lines[0].strip()[-3:] !='YES':
        time.sleep(0.2)
        lines = read_temp_raw_a
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000 + 0.7 # /1000 for correction into C, +/- calibration correction amount
        temp_c = str(round(temp_c, 2))
        return temp_c

#Create a list to store our results. List will be the same length as the number of devices we have
temps = {}#[0]*len(device_files)
start = time.time()

while True:
    timenow = time.asctime
    tstring = datetime.now().strftime("%Y-$m-%d-%H:%M:%S")
    tdur = time.time() - start

    for ds18b20 in ds18b20s.keys(): #device_num, device_file in enumerate(device_files):
        df = base_dir + "/" + ds18b20s[ds18b20] + "/w1_slave"#'/28-031197795ef3/w1_slave'
        temps[ds18b20] = get_temp(df)
        #     print all 3 to the terminal 2 decimal places
        #     append all 3 + experiment_name to the .csv for all experiments
        #     append all 3 + experiment_name to the .csv for this experiment
        # Experiment, Ambient, Above, Below, time_since_start, datetime
        

        #Read each device in turn and store the result to the results list.
        #temperature_results[device_num] = read_temp(device_file)
    print("({}) -{}- Ambient: {}, Above: {}, Below: {}".format(timenow, ename, temps["ambient"], temps["above"], temps["below"]))
    print("timenow: {}, tstring: {}, duration: {}".format(timenow, tstring, tdur))
    
    #print("Breadboard Probe 1 = ", temperature_results[0], " C")
    #print("Breadboard Probe 2 = ", temperature_results[0], " C") 
    time.sleep(3) #This is the pause between readings in seconds, there is lag induced by the 1w protocol
    
