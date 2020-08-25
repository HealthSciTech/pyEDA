# Importing necessary libraries
import numpy as np

def make_windows(data, sample_rate, windowsize=120, overlap=0, min_size=5):
    '''slices data into windows
    Funcion that slices data into windows. 
    
    Parameters
    ----------
    data : 1-d array 
        array containing gsr data
    sample_rate : int or float
        sample rate of the data stream in 'data'
    windowsize : int 
        size of the window that is sliced in seconds
    overlap : float
        fraction of overlap between two adjacent windows: 0 <= float < 1.0
    min_size : int 
        the minimum size for the last (partial) window to be included.
    
    Returns
    -------
    out : array
        tuples of window indices
    '''	
    ln = len(data)	
    window = windowsize * sample_rate
    stepsize = (1 - overlap) * window
    start = 0
    end = window
	    
    slices = []
    while end < len(data):
        slices.append((start, end))
        start += stepsize
        end += stepsize
    
    if min_size == -1: 
        slices[-1] = (slices[-1][0], len(data))
    elif (ln - start) / sample_rate >= min_size:
        slices.append((start, ln))
        
    return np.array(slices, dtype=np.int32)

	
def append_dict(dict, key, value):
    '''appends data to dict.
    Function that appends key to dict, if doesn't exist.
	
    Parameters
    ----------
    dict : dictionary
        dictionary object that contains continuous output measures
    key : String 
        key for the measure to be stored in continuous_dict
    value : any data container
        value to be appended to dictionary
		
    Returns
    -------
    dict : dict
        dictionary object passed to function, with specified data container appended
    ''' 
    try:
        dict[key].append(value)
    except KeyError:
        dict[key] = [value]
    return dict