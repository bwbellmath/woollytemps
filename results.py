import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt

# constants
dinterval = 500
cinterval = 10
dtolerance = 1.0
abdt = 1.0
bedt = 2.0
HUGE = 1000000.0
TEENY_WEENY = 0.000001


# read the .csv files
fi = "log/temps.csv"
di = pd.read_csv(fi)
#plt.plot(di[" time_since_start"], di[" Ambient"], color="blue")

experiments = di["Experiment"].unique()
#experiments = experiments[-1:]
di["mam"], di["bam"] = 0.0, 0.0
di["mab"], di["bab"] = 0.0, 0.0
di["mbe"], di["bbe"] = 0.0, 0.0
di["mmam"] = 0.0
di["mmab"] = 0.0
di["mmbe"] = 0.0

# TODO : if experiments.csv exists, read it and check that we have the required headers
# TODO : if all checks out, only perform experiments that 
# dataframe for the experiments
edf = pd.DataFrame({"Experiment" : experiments})
edf["eq_start"] = 0.0
edf["eq_end"] = HUGE
edf["beab_max"] = 0.0
edf["beab_min"] = 0.0
edf["beab_mean"] = 0.0
edf["abam_max"] = 0.0
edf["abam_min"] = 0.0
edf["abam_mean"] = 0.0
edf["ab_slope_max"] = 0.0
edf["be_slope_max"] = 0.0
edf["beab-abam_max"] = 0.0 # difference between differences
edf["beab-abam_min"] = 0.0
edf["beab-abam_mean"] = 0.0
edf["ab_time_10deg"] = 0.0
edf["be_time_10deg"] = 0.0
edf["analyze"] = 1 # 0 - don't, 1 - do, 2 - done and don't do again

for experiment in experiments:
  dis = di[di["Experiment"] == experiment]
  # loop through the time intervals
  abtim = HUGE
  betim = HUGE
  # prep print which experiment we're trying
  for i in range(len(dis)):
    if (i < dinterval):
      dint = i
    else:
      dint = dinterval-1
     
    diss = dis.loc[dis.index[i-dint:i+1]]
    if (len(diss) < 10):
      mam, mab, mbe = 0.0, 0.0, 0.0
      bam = np.mean(diss[" Ambient"])
      bab = np.mean(diss[" Above"])
      bbe = np.mean(diss[" Below"])
    else:
      mam, bam = np.polyfit(diss[" time_since_start"], diss[" Ambient"], 1)
      mab, bab = np.polyfit(diss[" time_since_start"], diss[" Above"], 1)
      mbe, bbe = np.polyfit(diss[" time_since_start"], diss[" Below"], 1)
    mmam = np.mean(diss[" Ambient"])
    mmab = np.mean(diss[" Above"])
    mmbe = np.mean(diss[" Below"])
    
    abtims = diss.loc[diss[" Above"] > diss.loc[diss.index[0]][" Above"]+abdt][" time_since_start"]
    betims = diss.loc[diss[" Above"] > diss.loc[diss.index[0]][" Above"]+bedt][" time_since_start"]
    # find the first index 10 higher than this one
    if (len(abtims) > 0):
      abtim = np.min([np.float(abtim), abtims[abtims.index[0]] - diss.loc[diss.index[0]][" time_since_start"]])
    if (len(betims) > 0):
      betim = np.min([betim, betims[betims.index[0]] - diss.loc[diss.index[0]][" time_since_start"]])
      # if there's none, return HUGE
    abcsum = np.cumsum(diss[" Above"])
    becsum = np.cumsum(diss[" Below"])
    di.loc[dis.index[i], ["mam", "bam"]] = mam, bam
    di.loc[dis.index[i], ["mab", "bab"]] = mab, bab
    di.loc[dis.index[i], ["mbe", "bbe"]] = mbe, bbe
    di.loc[dis.index[i], ["mmam", "mmab", "mmbe"]] = mmam, mmab, mmbe
    

  # Done : plot difference between below and above
  #                         ambient and above
  # Done : plot difference between ambient and below (transparent)
  # label all plots
  # Done : plot 100 time moving average
  
  # metrics:
  # Identify stable period
  #   below is at least 40 degrees
  #   500 moving average slope is below 0.0006
  dis = di[di["Experiment"] == experiment]
  sinds = dis.index[((dis["mmbe"] > 40) & (np.abs(dis["mbe"]) < 0.0006))]
  sdis = dis.loc[sinds]
  if (len(sdis) < 1):
    print(F"No Stable Region Detected, Skipping {experiment}")
    edf.loc[edf.index[edf["Experiment"] == experiment], ["analyze"]] = 0
    continue
  sdis["mmbeab"] = sdis["mmbe"] - sdis["mmab"]
  sdis["mmabam"] = sdis["mmab"] - sdis["mmam"]
  sdis["beab_abam"] = sdis["mmbeab"]-sdis["mmabam"]

  edf.loc[edf.index[edf["Experiment"] == experiment], ["eq_start"]] = sdis.loc[sdis.index[0]][" time_since_start"]
  edf.loc[edf.index[edf["Experiment"] == experiment], ["eq_end"]] = sdis.loc[sdis.index[-1]][" time_since_start"]
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab_max"]] = sdis["mmbeab"].max()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab_min"]] = sdis["mmbeab"].min()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab_mean"]] = sdis["mmbeab"].mean()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["abam_max"]] = sdis["mmbeab"].max()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["abam_min"]] = sdis["mmbeab"].min()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["abam_mean"]] = sdis["mmbeab"].mean()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["ab_slope_max"]] = sdis["mab"].max()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["be_slope_max"]] = sdis["mbe"].max()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab-abam_max"]] = sdis["beab_abam"].max() # difference between differences
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab-abam_min"]] = sdis["beab_abam"].min()
  edf.loc[edf.index[edf["Experiment"] == experiment], ["beab-abam_mean"]] = sdis["beab_abam"].mean
  edf.loc[edf.index[edf["Experiment"] == experiment], ["ab_time_10deg"]] = abtim
  edf.loc[edf.index[edf["Experiment"] == experiment], ["be_time_10deg"]] = betim
  edf.loc[edf.index[edf["Experiment"] == experiment], ["analyze"]] = 2

  # prep print this line from edf

  # max temperature difference above and below
  
  # min temperature difference above and below
  # mean temperature difference above and below


  #   maximum slope during heating above
  #   maximum slope during heating below
  #   average difference between differences
  #   minimum difference between differences
  # compute shortest time to raise by x degrees

  # prep plot each of the figures
  plt.figure(1)

  plt.plot(dis[" time_since_start"], dis[" Ambient"],
           color="blue", label="Ambient")
  plt.plot(dis[" time_since_start"], dis[" Above"],
           color="red", label="Above")
  plt.plot(dis[" time_since_start"], dis[" Below"],
           color="orange", label = "Below")
  plt.plot(dis[" time_since_start"], dis[" Below"]-dis[" Above"],
           color="purple", label="Be - Ab")  
  plt.plot(dis[" time_since_start"], dis[" Above"]-dis[" Ambient"],
           color="green", label="Ab - Am")  
  plt.plot(dis[" time_since_start"], dis["mmam"],
           color="blue", alpha = 0.4, label="Am Mvg Avg")
  plt.plot(dis[" time_since_start"], dis["mmab"],
           color="red", alpha = 0.4, label="Ab Mvg Avg")
  plt.plot(dis[" time_since_start"], dis["mmbe"],
           color="orange", alpha = 0.4, label="Be Mvg Avg")
  plt.axvline(x=sdis.loc[sdis.index[0]][" time_since_start"])
  plt.axvline(x=sdis.loc[sdis.index[-1]][" time_since_start"])
  plt.legend()
  plt.title(experiment)
  #plt.show()

  # separately plot the slopes
  plt.figure(2)
  plt.plot(dis[" time_since_start"], dis["mam"], color="blue")
  plt.plot(dis[" time_since_start"], dis["mab"], color="red")  
  plt.plot(dis[" time_since_start"], dis["mbe"], color="orange")
  plt.title(F"{experiment}-slopes")
  plt.axvline(x=sdis.loc[sdis.index[0]][" time_since_start"])
  plt.axvline(x=sdis.loc[sdis.index[-1]][" time_since_start"])

  #plt.show()
  # separately plot the intercepts (adjust to make these means...)
  plt.figure(3)
  plt.plot(dis[" time_since_start"], dis["bam"], color="blue")
  plt.plot(dis[" time_since_start"], dis["bab"], color="red")  
  plt.plot(dis[" time_since_start"], dis["bbe"], color="orange")
  plt.title(F"{experiment}-intercepts")
  plt.axvline(x=sdis.loc[sdis.index[0]][" time_since_start"])
  plt.axvline(x=sdis.loc[sdis.index[-1]][" time_since_start"])

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
# prep when we're all done, print etf table

fo = "log/experiments.csv"
edf.to_csv(fo)
