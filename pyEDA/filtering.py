# Importing necessary libraries
from scipy.signal import butter, filtfilt
  
'''
Low pass filter to remove noise specially artifact noise
'''
def butter_lowpassfilter(data, cutoff, sample_rate, order=2):
  '''standard lowpass filter.
    Function that filters the data using standard Butterworth lowpass filter
	
    Parameters
    ----------
	data : 1-d array
        array containing the gsr data
    cutoff : int or float
        frequency in Hz that acts as cutoff for filter.
    sample_rate : int or float
        sample rate of the supplied signal
    order : int
        filter order, defines the strength of the roll-off
        around the cutoff frequency.
        default: 2
    
    Returns
    -------
    y : 1-d array
        filtered gsr data
  '''
  nyq = 0.5 * sample_rate
  normal_cutoff = cutoff/nyq
  b, a = butter(order, normal_cutoff, btype='low', analog=False)
  y = filtfilt(b, a, data)
  return y