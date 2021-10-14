import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt

# constants
dinterval = 100
cinterval = 10
dtolerance = 1.0


# read the .csv files
fi = "log/temps.csv"
di = pd.read_csv(fi)
plt.plot(di[" time_since_start"], di[" Ambient"], color="blue")

experiments = di["Experiment"].unique()
di["mam"], di["bam"] = 0.0, 0.0
di["mab"], di["bab"] = 0.0, 0.0
di["mbe"], di["bbe"] = 0.0, 0.0
for experiment in experiments:
  dis = di[di["Experiment"] == experiment]
  # loop through the time intervals
  for i in range(len(dis)-dinterval):
    diss = dis.loc[dis.index[np.arange(i,i+dinterval)]]
    mam, bam = np.polyfit(diss[" time_since_start"], diss[" Ambient"], 1)
    mab, bab = np.polyfit(diss[" time_since_start"], diss[" Above"], 1)
    mbe, bbe = np.polyfit(diss[" time_since_start"], diss[" Below"], 1)
    di.loc[dis.index[i+dinterval], ["mam", "bam"]] = mam, bam
    di.loc[dis.index[i+dinterval], ["mab", "bab"]] = mab, bab
    di.loc[dis.index[i+dinterval], ["mbe", "bbe"]] = mbe, bbe

  dis = di[di["Experiment"] == experiment]
  plt.plot(dis[" time_since_start"], dis[" Ambient"], color="blue")
  plt.plot(dis[" time_since_start"], dis[" Above"], color="red")  
  plt.plot(dis[" time_since_start"], dis[" Below"], color="orange")
  plt.title(experiment)
  plt.show()

  # separately plot the slopes
  plt.plot(dis[" time_since_start"], dis["mam"], color="blue")
  plt.plot(dis[" time_since_start"], dis["mab"], color="red")  
  plt.plot(dis[" time_since_start"], dis["mbe"], color="orange")
  plt.title(F"{experiment}-slopes")
  plt.show()
  # separately plot the intercepts (adjust to make these means...)
  plt.plot(dis[" time_since_start"], dis["bam"], color="blue")
  plt.plot(dis[" time_since_start"], dis["bab"], color="red")  
  plt.plot(dis[" time_since_start"], dis["bbe"], color="orange")
  plt.title(F"{experiment}-intercepts")
  plt.show()



# read config file with descriptions?
# get configurations
# create a table with conf info for each sample
# generate plots
# generate statistics
# dump table, descriptions, plots, and statistics to markdown file
# generate ranking summary (sorted by total insulative value but also with insulative value normalized by sample mass

# dump ranking to final file
# dump summary file on top of final file
# dump summary tail. 
