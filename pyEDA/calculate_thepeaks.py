# Importing necessary libraries
import numpy as np

'''
Calculate the number of peaks based on onSet and offSet values.
'''
def calculate_thepeaks(normalized_gsr, onSet_offSet, ampThreshold=0.02):
  # Some initializations
  peaklist = []
  indexlist = []
  checkForMax = False
  peakIndex = 0
  index = 0
  Max = 0

  for i, data in enumerate(normalized_gsr):
    if (index == len(onSet_offSet)):
      break
    if (checkForMax):
      startIndex = onSet_offSet[index][0]
      amplitude = data-normalized_gsr[startIndex]
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