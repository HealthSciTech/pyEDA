# Importing necessary libraries
import numpy as np

'''
Calculate the list of on-sets and off-sets based on phasic component of signal.
'''
def calculate_onSetOffSet(phasic_gsr, sample_rate, minDiff=0.5, onSetThreshold=0.01):
  '''finding on-sets and off-sets
    Funcion that finds the on-sets and offsets of gsr data using phasic component
    
    Parameters
    ----------
    phasic_gsr : 1-d array 
        array containing phasic component of gsr
	sample_rate : int or float
        sample rate of the data stream in 'data'
    minDiff : float
        minimum acceptable time difference between on-set and off-set
        default : 0.02
    onSetThreshold : float 
        on set threshold
        default : 0.02
    
    Returns
    -------
    peaklist : 2-d array
        list of peaks for each onSet-offSet window
	indexlist : 2-d array
        list of indexes peaks for each onSet-offSet window
  '''
  # Some initializations
  onSet_offSet = []
  tmpSet = []
  onIsSet = False

  for i, data in enumerate(phasic_gsr):
    if (onIsSet):
      if (data < 0):
        tmpSet.append(i)
        timeDifference = tmpSet[1]-tmpSet[0]
        timeDifference = timeDifference/sample_rate
        if (timeDifference > minDiff):
          onSet_offSet.append(tmpSet)
        tmpSet = []
        onIsSet = False
    elif data > onSetThreshold:
      tmpSet.append(i)
      onIsSet = True

  return np.array(onSet_offSet)