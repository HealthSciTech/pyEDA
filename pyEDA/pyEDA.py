'''
process EDA signal without windowing
returns only one value for each feature
'''
def process(gsrdata, sample_rate, windowsize=0.75, report_time=False,  
            measures={}, working_data={}):
    '''processes passed gsrdata.
    
    Processes the passed gsr data. Returns measures{} dict containing results.
    Parameters
    ----------
    gsrdata : 1d array or list 
        array or list containing gsr data to be analysed
    sample_rate : int or float
        the sample rate with which the gsr data is sampled
    windowsize : int or float
        the window size in seconds to use in the calculation of the moving average.
        Calculated as windowsize * sample_rate
        default : 0.75
    report_time : bool
        whether to report total processing time of algorithm 
        default : True
    measures : dict
        dictionary object used by heartpy to store computed measures. Will be created
        if not passed to function.
    working_data : dict
        dictionary object that contains all heartpy's working data (temp) objects.
        will be created if not passed to function
    Returns
    -------
    working_data : dict
        dictionary object used to store temporary values.
    
    measures : dict
        dictionary object used by heartpy to store computed measures.
    '''
    t1 = time.perf_counter()

    assert np.asarray(gsrdata).ndim == 1, 'error: multi-dimensional data passed to process() \
function. Please supply a 1d array or list containing heart rate signal data. \n\nDid you perhaps \
include an index column?'
    # Filtered gsr for finding peaks
    filtered_gsr = butter_lowpassfilter(gsrdata, 5/sample_rate, sample_rate, order=2)
    # Passing the rolling window from the gsrdata 
    rol_mean = rolling_mean(gsrdata, windowsize, sample_rate)
    # Normalized the rol_mean
    normalized_gsr = normalization(rol_mean)
    # Passing the gsrdata from median filter    
    #medfilt_gsr = medfilt(normalized_gsr)
    # Extract phasic gsr signal from original signal
    #phasic_gsr = median_filter(normalized_gsr, sample_rate)
    [phasic_gsr, p, tonic_gsr, l, d, e, obj] = cvxEDA(normalized_gsr, 1./sample_rate)    
    filtered_phasic_gsr = butter_lowpassfilter(phasic_gsr, 5/sample_rate, sample_rate, order=2)

    # Update working_data
    working_data['gsr'] = gsrdata
    working_data['filtered_gsr'] = filtered_gsr
    working_data['rol_mean'] = rol_mean
    working_data['normalized_gsr'] = normalized_gsr
    working_data['filtered_phasic_gsr'] = filtered_phasic_gsr
    working_data['phasic_gsr'] = phasic_gsr
    working_data['tonic_gsr'] = tonic_gsr

    # Calculate the onSet and offSet based on Phasic GSR signal
    onSet_offSet = calculate_onSetOffSet(filtered_phasic_gsr, sample_rate)
    print(onSet_offSet)
    # Calculate the peaks using onSet and offSet of Phasic GSR signal
    if (len(onSet_offSet) != 0):
      peaklist, indexlist = calculate_thepeaks(normalized_gsr, onSet_offSet)
    else: 
      peaklist = []
      indexlist = []
    working_data['peaklist'] = peaklist
    working_data['indexlist'] = indexlist
    # Calculate the number of peaks
    measures['number_of_peaks'] = calculate_number_of_peaks(peaklist)
    # Calculate the mean and the max of EDA from the original GSR signal
    measures['mean'] = calculate_mean(normalized_gsr)
    measures['max'] = calculate_max(normalized_gsr)

    #report time if requested. Exclude from tests, output is untestable.
    if report_time: # pragma: no cover
        print('\nFinished in %.8s sec' %(time.perf_counter()-t1))

    return working_data, measures

	

'''
process EDA signal with windowing of size segment_width*sample_rate
'''
def process_segmentwise(gsrdata, sample_rate, segment_width=120, segment_overlap=0,
                        segment_min_size=20, **kwargs):
    '''processes gsr data with a windowed function
    Analyses a long gsr data array by running a moving window 
    over the data, computing measures in each iteration. Both the window width
    and the overlap with the previous window location are settable.
    Parameters
    ----------
    gsrdata : 1d array or list 
        array or list containing gsr data to be analysed
    sample_rate : int or float
        the sample rate with which the gsr data is sampled
    segment_width : int or float
        width of segments in seconds
        default : 120
    segment_overlap: float
        overlap fraction of adjacent segments.
        Needs to be 0 <= segment_overlap < 1.
        default : 0 (no overlap)
    segment_min_size : int
        often a tail end of the data remains after segmenting into segments.
        segment_min_size indicates the minimum length (in seconds) the tail 
        end needs  to be in order to be included in analysis. It is discarded 
        if it's shorter.
        default : 20
    Keyword arguments:
    ------------------
    gsrdata -- 1-dimensional numpy array or list containing gsr data
    sample_rate -- the sample rate of the gsr data
    segment_width -- the width of the segment, in seconds, within which all measures 
                     will be computed.
    segment_overlap -- the fraction of overlap of adjacent segments, 
                       needs to be 0 <= segment_overlap < 1
    segment_min_size -- After segmenting the data, a tail end will likely remain that is shorter than the specified
                        segment_size. segment_min_size sets the minimum size for the last segment of the 
                        generated series of segments to still be included. Default = 20.
    Returns
    -------
    working_data : dict
        dictionary object used to store temporary values.
    
    measures : dict
        dictionary object used to store computed measures.
    '''

    assert 0 <= segment_overlap < 1.0, 'value error: segment_overlap needs to be \
0 <= segment_overlap < 1.0!'

    s_measures={}
    s_working_data={}

    slice_indices = make_windows(gsrdata, sample_rate, segment_width, segment_overlap, segment_min_size)

    for i, ii in slice_indices:
        try:
            working_data, measures = process(gsrdata[i:ii], sample_rate, **kwargs)
            for k in measures.keys():
                s_measures = append_dict(s_measures, k, measures[k])
            for k in working_data.keys():
                s_working_data = append_dict(s_working_data, k, working_data[k])
            s_measures = append_dict(s_measures, 'segment_indices', (i, ii))
            s_working_data = append_dict(s_working_data, 'segment_indices', (i, ii))
        except exceptions.BadSignalWarning:
            pass

    return s_working_data, s_measures