# Importing necessary libraries
import numpy as np

def calculate_max_peaks(data):
  if (len(data) == 0):
    return 0
  else:
    return np.max(data)
  
def calculate_mean_gsr(data):
  return np.mean(data)
  
def calculate_number_of_peaks(data):
  return len(data)