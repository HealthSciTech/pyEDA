def resample_data(gsrdata, prevSR, newSR):
	number_of_samples = round(len(gsrdata) * float(newSR) / prevSR)
	data = sps.resample(gsrdata, number_of_samples)
	return data

	
def normalization(gsrdata):
    gsrdata = gsrdata-(np.min(gsrdata))
    gsrdata /= (np.max(gsrdata) - np.min(gsrdata))
    return gsrdata
	
	
def _sliding_window(data, windowsize):
    '''segments data into windows
    Function to segment data into windows for rolling mean function.
    Function returns the data segemented into sections.
    Parameters
    ----------
    data : 1d array or list
        array or list containing data over which sliding windows are computed
    windowsize : int
        size of the windows to be created by the function
    Returns
    -------
    out : array of arrays
        data segmented into separate windows.
    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> windows = _sliding_window(data, windowsize = 3)
    >>> windows.shape
    (3, 3)
    '''
    shape = data.shape[:-1] + (data.shape[-1] - windowsize + 1, windowsize)
    strides = data.strides + (data.strides[-1],)
    return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)
		
		
def rolling_mean(data, windowsize, sample_rate):
    '''calculates rolling mean
    Function to calculate the rolling mean (also: moving average) over the passed data.
    Parameters
    ----------
    data : 1-dimensional numpy array or list
        sequence containing data over which rolling mean is to be computed
    windowsize : int or float 
        the window size to use, in seconds 
        calculated as windowsize * sample_rate
    sample_rate : int or float
        the sample rate of the data set
    Returns
    -------
    out : 1-d numpy array
        sequence containing computed rolling mean
    '''
    avg_hr = (np.mean(data))
    data_arr = np.array(data)
    rol_mean = np.mean(_sliding_window(data_arr, int(windowsize*sample_rate)), axis=1)
    missing_vals = np.array([avg_hr for i in range(0, int(abs(len(data_arr) - len(rol_mean))/2))])
    rol_mean = np.insert(rol_mean, 0, missing_vals)
    rol_mean = np.append(rol_mean, missing_vals)

    #only to catch length errors that sometimes unexplicably occur. 
    ##Generally not executed, excluded from testing and coverage
    if len(rol_mean) != len(data): # pragma: no cover
        lendiff = len(rol_mean) - len(data)
        if lendiff < 0:
            rol_mean = np.append(rol_mean, 0)
        else:
            rol_mean = rol_mean[:-1]            
    return rol_mean