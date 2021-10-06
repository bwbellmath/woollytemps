# temps.py

# Identify the temperature sensors (map the addresses to names)
# prompt the user to name this experiment
# generate a .csv file for just this experiment
# While true, with some time delay,
#   sleep(10) sleep for 1000ms -- we only want one reading per second or maybe a half second. 
#   read the temps from all sensors and
#     print all 3 to the terminal 2 decimal places
#     append all 3 + experiment_name to the .csv for all experiments
#     append all 3 + experiment_name to the .csv for this experiment
#     If all 3 sensors have been stable for a full minute, print "EQUILIBRIUM REACHED"
#       i.e. if all 3 sensors have max - min over the last n (5 minutes worth) values < epsilon = 1.0 degrees
