# Importing necessary libraries
import numpy as np
import time
import scipy.signal
import matplotlib.pyplot as plt
from scipy import stats

# Importing necessary functions
from pyEDA.pyEDA.calculate_onSetOffSet import *
from pyEDA.pyEDA.calculate_thepeaks import *
from pyEDA.pyEDA.calculateFeatures import *
from pyEDA.pyEDA.cvxEDA import *
from pyEDA.pyEDA.filtering import *
from pyEDA.pyEDA.preprocessing import *
from pyEDA.pyEDA.windowing import *

'''

'''
def statistical_feature_extraction(preprocessed_gsr, sample_rate, windowsize=0.75,  use_scipy=True, measures={},
                        working_data={}):
	'''processes passed gsrdata.
	
	Processes the passed gsr data. Returns measures{} dict containing results.
	Parameters
	----------
	preprocessed_gsr : 1d array or list 
		array or list containing normalized gsr data to be analysed
	sample_rate : int or float
		the sample rate with which the gsr data is sampled
	windowsize : int or float
		the window size in seconds to use in the calculation of the moving average.
		Calculated as windowsize * sample_rate
		default : 0.75
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
	t1 = time.time()
	
	
	# Extracting phasic and tonic components of from normalized gsr
	[phasic_gsr, p, tonic_gsr, l, d, e, obj] = cvxEDA(preprocessed_gsr, 1./sample_rate)
	
	# Removing line noise
	filtered_phasic_gsr = butter_lowpassfilter(phasic_gsr, 5./sample_rate, sample_rate, order=4)
	
	# Update working_data
	working_data['filtered_phasic_gsr'] = filtered_phasic_gsr
	working_data['phasic_gsr'] = phasic_gsr
	working_data['tonic_gsr'] = tonic_gsr
	
	peaklist = []
	indexlist = []
	
	if (use_scipy):
		indexlist, _ = scipy.signal.find_peaks(filtered_phasic_gsr)
		for i in indexlist:
			peaklist.append(preprocessed_gsr[i])
	else:
		# Calculate the onSet and offSet based on Phasic GSR signal
		onSet_offSet = calculate_onSetOffSet(filtered_phasic_gsr, sample_rate)
		# Calculate the peaks using onSet and offSet of Phasic GSR signal
		if (len(onSet_offSet) != 0):
			peaklist, indexlist = calculate_thepeaks(preprocessed_gsr, onSet_offSet)
	
	working_data['peaklist'] = peaklist
	working_data['indexlist'] = indexlist
	# Calculate the number of peaks
	measures['number_of_peaks'] = calculate_number_of_peaks(peaklist)
	# Calculate the std mean of EDA
	measures['mean_gsr'] = calculate_mean_gsr(preprocessed_gsr)
	# Calculate the maximum value of peaks of EDA
	measures['max_of_peaks'] = calculate_max_peaks(peaklist)
	
	return working_data, measures

	

'''
process EDA signal with windowing of size segment_width*sample_rate
'''
def segmentwise(gsrdata, sample_rate, segment_width=120, segment_overlap=0,
                        segment_min_size=5):
	'''processes passed gsrdata.
	Processes the passed gsr data. Returns measures{} dict containing results.
	
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
		default : 20
	
	Returns
	-------
	gsrdata_segmentwise : 2d array or list 
		array or list containing segmentwised gsr data to be analysed
	orking_data : dict
		dictionary object used to store temporary values.
	s_measures : dict
		dictionary object used by heartpy to store computed measures.
	'''
	slice_indices = make_windows(gsrdata, sample_rate, segment_width, segment_overlap, segment_min_size)
	
	s_measures = {}
	s_working_data = {}
	
	gsrdata_segmentwise = []
	for i, ii in slice_indices:
		gsrdata_segmentwise.append(gsrdata[i:ii])
		s_measures = append_dict(s_measures, 'segment_indices', (i, ii))
		s_working_data = append_dict(s_working_data, 'segment_indices', (i, ii))
	return s_working_data, s_measures, gsrdata_segmentwise
