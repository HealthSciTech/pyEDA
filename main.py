# Importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

# Importing necessary functions for feature extraction
from pyEDA.openShimmerFile import *
from pyEDA.preprocessing import *
from pyEDA.filtering import *
from pyEDA.pyEDA import *
from pyEDA.DNN_Features import *

def process(gsr_signal, use_scipy=True, sample_rate=128, new_sample_rate=40, segment_width=600, segment_overlap=0):
	gsrdata = np.array(gsr_signal)
	
	plt.figure(figsize=(12,4))
	plt.plot(gsrdata)
	plt.show()
	
	print("If you are using this tool for your research please cite this paper: \"GSR Analysis for Stress: Development and Validation of an Open Source Tool for Noisy Naturalistic GSR Data\"");
	
	############################################################################
	############################ Preprocessing Part ############################
	
	# Select the new sample rate, and windowing size
	new_sample_rate = new_sample_rate
	segment_width = segment_width
	
	# Resample the data based on original data rate of your device, here: 128Hz
	data = resample_data(gsrdata, sample_rate, new_sample_rate)
	
	# Segmentwise the data based on window sizes
	s_working_data, s_measures, gsrdata_segmentwise = segmentwise(data, sample_rate=new_sample_rate, segment_width=segment_width, segment_overlap=segment_overlap)
	
	preprocessed_gsr = []
	for i in gsrdata_segmentwise:
		preprocessed_gsr.append(normalization(rolling_mean(i, 1./new_sample_rate, new_sample_rate)))
	
	############################ Preprocessing Part ############################
	############################################################################
	
	
	
	#################################################################################
	############################ Feature Extraction Part ############################
	
	# Statistical Feature Extraction
	for i in preprocessed_gsr:
		working_data, measures = statistical_feature_extraction(i, new_sample_rate, use_scipy=use_scipy)
		for k in measures.keys():
			s_measures = append_dict(s_measures, k, measures[k])
		for k in working_data.keys():
			s_working_data = append_dict(s_working_data, k, working_data[k])
	
	wd = s_working_data
	m = s_measures
	
	"""
	# Deep Learning Feature Extraction
	# Just Need to load the trained model here and use it for prediction: 
	# The current model is trained for stress detection feature extraction (WESAD dataset)
	for i in preprocessed_gsr:
		model = create_1Dcnn(len(i))
		path_to_DL_weights = './pyEDA/eda_deep_model.h5'
		model.load_weights(path_to_DL_weights)
		
		# Features extracted from Deep learning model
		getFeature = deepFeatures(model)
		
		# Fully Connected Network which can be used for the prediction
		getPrediction = deepPrediction(model)"""
		
	############################ Feature Extraction Part ############################
	#################################################################################
	
	return m, wd