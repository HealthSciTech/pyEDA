'''
Using median filter to extract phasic component of gsr
'''
def median_filter(normalized_gsr, sample_rate):
  distance = 4*sample_rate
  for i,j in enumerate(normalized_gsr):
    t1 = i-distance
    t2 = i+distance
    if (t1 < 0):
      t1 = 0
    if (t2 > len(normalized_gsr)-1):
      t2 = len(normalized_gsr)-1
    
    normalized_gsr[i] = normalized_gsr[i]-median(normalized_gsr[t1:t2])

  return normalized_gsr
  
'''
Low pass filter to remove noise specially artifact noise
'''
def butter_lowpass(cutoff, sample_rate, order=2):
    '''standard lowpass filter.
    Function that defines standard Butterworth lowpass filter
    Parameters
    ----------
    cutoff : int or float
        frequency in Hz that acts as cutoff for filter.
        All frequencies above cutoff are filtered out.
    sample_rate : int or float
        sample rate of the supplied signal
    order : int
        filter order, defines the strength of the roll-off
        around the cutoff frequency. Typically orders above 6
        are not used frequently.
        default: 2
    
    Returns
    -------
    out : tuple
        numerator and denominator (b, a) polynomials
        of the defined Butterworth IIR filter.
    '''
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpassfilter(data, cutoff, sample_rate, order=2):
    b, a = butter_lowpass(cutoff, sample_rate, order=order)
    y = filtfilt(b, a, data)
    return y