# Importing necessary libraries
import numpy as np

'''
Calculate the number of peaks based on on-set and off-set values.
'''
def calculate_thepeaks(gsr, onSet_offSet, ampThreshold=0.02):
  '''calculate the peaks
    Funcion that finds the peaks in each on-set off-set window
    
    Parameters
    ----------
    gsr : 1-d array 
        array containing gsr sensor data
    onSet_offSet : 2-d array
        array containing the onSet and offSet for each window
    ampThreshold : float 
        amplitude threshold
        default : 0.02
    
    Returns
    -------
    peaklist : 2-d array
        list of peaks for each onSet-offSet window
    indexlist : 2-d array
        list of indexes peaks for each onSet-offSet window
  '''
  # Some initializations
  peaklist = []
  indexlist = []
  checkForMax = False
  peakIndex = 0
  index = 0
  Max = 0

  for i, data in enumerate(gsr):
    if (index == len(onSet_offSet)):
      break
    if (checkForMax):
      startIndex = onSet_offSet[index][0]
      amplitude = data-gsr[startIndex]
      if (amplitude > Max):
        peakIndex = i
        Max = amplitude
      if (i == onSet_offSet[index][1]):
        # Check the threshold and add the peak to peaklist
        if (Max > ampThreshold):
          peaklist.append(Max)
          indexlist.append(peakIndex)
        Max = 0
        checkForMax = False
        index=index+1
    elif (i == onSet_offSet[index][0]):
      checkForMax = True

  return np.array(peaklist), np.array(indexlist)