# Importing necessary libraries
import csv
import time
import glob
import datetime
import math
import cvxopt.solvers
import scipy.signal as sps
import cvxopt as cv
import heartpy as hp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from statistics import median
from scipy.interpolate import UnivariateSpline, interp1d
from scipy.signal import medfilt, resample, butter, filtfilt, iirnotch, savgol_filter

# Importing necessary functions
from calculate_onSetOffSet import *
from calculate_thepeaks import *
from calculateFeatures import *
from cvxEDA import *
from filtering import *
from openShimmerFile import *
from preprocessing import *
from windowing import *
from pyEDA import *

# You must edit these based on your file
fileName = '110_Session1_Shimmer_9301_Calibrated_PC.csv'
columnName = 'Shimmer_9301_GSR_Skin_Conductance_CAL'

Raw_GSR = openShimmerFile(fileName, columnName)

# Visualise the data
gsrdata = np.array(Raw_GSR)
plt.figure(figsize=(12,4))
plt.plot(gsrdata)
plt.figure(figsize=(12,4))
plt.show()

# Select the new sample rate, and windowing size
sample_rate=40
segment_width=500

# Resample the data based on original data rate of your device, here: 128Hz
data = resample_data(gsrdata, 128, sample_rate)

# Process the whole data without windowing
# wd, m = process(data, sample_rate)

# Process the whole data with windowing
wd, m = process_segmentwise(data, sample_rate=sample_rate, segment_width=segment_width, segment_overlap=0)

# Mapping the indexlist of each window to original data: comment it if you do not use windowing
for index,i in enumerate(wd['indexlist']):
  for index2,j in enumerate(i):
    wd['indexlist'][index][index2] = j+segment_width*sample_rate*index
	
# Storing the peaks for visualization
peaks = []
for index,i in enumerate(wd['indexlist']):
  for index2,j in enumerate(i):
    peaks.append(j)
	
# Visualize the data with detected peaks marked with "x"
plt.plot(data)
plt.plot(peaks, data[peaks], "x")
plt.show()