# Importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

# Importing necessary functions for feature extraction
from pyEDA.pyEDA.openShimmerFile import *
from pyEDA.pyEDA.preprocessing import *
from pyEDA.pyEDA.filtering import *
from pyEDA.pyEDA.pyEDA import *
from pyEDA.pyEDA.autoencoder import *

def process_statistical(gsr_signal, use_scipy=True, sample_rate=128, new_sample_rate=40, segment_width=600, segment_overlap=0):
	gsrdata = np.array(gsr_signal)
	
	print("If you are using this tool for your research please cite this paper: \"pyEDA: An Open-Source Python Toolkit for Pre-processing and Feature Extraction of Electrodermal Activity\"");
	
	#################################################################################
	############################## Preprocessing Part ###############################
	
	# Resample the data based on original data rate of your device, here: 128Hz
	data = resample_data(gsrdata, sample_rate, new_sample_rate)
	
	# Segmentwise the data based on window sizes
	s_working_data, s_measures, gsrdata_segmentwise = segmentwise(data, sample_rate=new_sample_rate, segment_width=segment_width, segment_overlap=segment_overlap)
	
	preprocessed_gsr = []
	for i in gsrdata_segmentwise:
		preprocessed_gsr.append(rolling_mean(i, 1./new_sample_rate, new_sample_rate))
	
	############################## Preprocessing Part ###############################
	#################################################################################
	
	
	
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
		
	############################ Feature Extraction Part ############################
	#################################################################################
	
	return m, wd, preprocessed_gsr
	
	
def prepare_automatic(gsr_signal, sample_rate=128, new_sample_rate=40, k=32, epochs=100, batch_size=10):
	gsrdata = np.array(gsr_signal)
	print("If you are using this tool for your research please cite this paper: \"pyEDA: An Open-Source Python Toolkit for Pre-processing and Feature Extraction of Electrodermal Activity\"");
	
	#################################################################################
	############################## Preprocessing Part ###############################
	
	# Resample the data based on original data rate of your device, here: 128Hz + rolling window
	
	preprocessed_gsr = []
	for i in gsr_signal:
		data = resample_data(i, sample_rate, new_sample_rate)
		preprocessed_gsr.append(rolling_mean(data, 1./new_sample_rate, new_sample_rate))
	preprocessed_gsr = np.array(preprocessed_gsr)
	
	############################## Preprocessing Part ###############################
	#################################################################################
	
	
	#################################################################################
	############################ Train the Autoencoder ##############################
	
	# set the input shape to model
	input_shape = preprocessed_gsr.shape[1]
	
	#  use gpu if available
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	# create a model from `AE` autoencoder class
	# load it to the specified device, either gpu or cpu
	model = AE(input_shape=input_shape, latent_size=k).to(device)

	# create an optimizer object
	# Adam optimizer with learning rate 1e-3
	optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

	# mean-squared error loss
	criterion = nn.MSELoss()
	
	# create tensor data
	train_loader = create_train_loader(preprocessed_gsr, batch_size)
	
	# Training the network
	for epoch in range(epochs):
		loss = 0
		for batch_features in train_loader:
			# reset the gradients back to zero
			# PyTorch accumulates gradients on subsequent backward passes
			optimizer.zero_grad()
			# compute reconstructions
			outputs,_ = model(batch_features)
			
			# compute training reconstruction loss
			train_loss = criterion(outputs, batch_features)
			
			# compute accumulated gradients
			train_loss.backward()
			
			# perform parameter update based on current gradients
			optimizer.step()
			
			# add the mini-batch training loss to epoch loss
			loss += train_loss.item()
			
		# compute the epoch training loss
		loss = loss / len(train_loader)
		
		# display the epoch training loss
		print("epoch : {}/{}, loss = {:.6f}".format(epoch + 1, epochs, loss))
		
	# Save the network
	torch.save(model, 'pyEDA\pyEDA\checkpoint.t7')
		
	############################ Train the Autoencoder ##############################
	#################################################################################
	

def process_automatic(gsr_signal):
	#################################################################################
	############################ Feature Extraction Part ############################
	
	# Load the network
	model = torch.load('pyEDA\pyEDA\checkpoint.t7')
	
	# Extract the features
	gsr_signal = np.reshape(gsr_signal, (1, gsr_signal.shape[0]))
	train_outputs, latent_variable = model(torch.FloatTensor(gsr_signal))
	return latent_variable.detach().numpy()[0];
	
	############################ Feature Extraction Part ############################
	#################################################################################
	
