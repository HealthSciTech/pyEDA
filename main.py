import sys
import os

# Importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

path = os.getcwd()+'\\pyEDA\\'
sys.path.insert(0, path)
# Importing necessary functions for feature extraction
from openShimmerFile import *
from preprocessing import *
from filtering import *
from pyEDA import *

path = os.getcwd()+'\\classification\\'
sys.path.insert(0, path)
# Importing necessary functions for classification
from knnClassifier import *
from NaiveBayesGaussianClassifier import *
from RandomForestClassifier import *
from SVMClassifier import *

path = os.getcwd()+'\\tournament_selection\\'
sys.path.insert(0, path)
# Importing necessary functions for final prediction
from TournamentSelection import *


# You must edit these based on your files
fileName = ['110_Session1_Shimmer_9301_Calibrated_PC.csv']
columnName = 'Shimmer_9301_GSR_Skin_Conductance_CAL'
X = [] # Input X for classifier
Y = [] # Target Y for input X

for i in fileName:
  Raw_GSR = openShimmerFile(i, columnName)
  gsrdata = np.array(Raw_GSR)
  
  #plt.figure(figsize=(12,4))
  #plt.plot(gsrdata)
  #plt.show()

  ############################################################################
  ############################ Preprocessing Part ############################
  
  # Select the new sample rate, and windowing size
  sample_rate=40
  segment_width=500

  # Resample the data based on original data rate of your device, here: 128Hz
  data = resample_data(gsrdata, 128, sample_rate)

  # Segmentwise the data based on window sizes
  s_working_data, s_measures, gsrdata_segmentwise = segmentwise(data, sample_rate=sample_rate, segment_width=segment_width, segment_overlap=0)
  
  normalized_gsr = []
  for i in gsrdata_segmentwise:
    normalized_gsr.append(normalization(rolling_mean(i, 1./sample_rate, sample_rate)))
	
  ############################ Preprocessing Part ############################
  ############################################################################
  
  
  
  #################################################################################
  ############################ Feature Extraction Part ############################

  # Statistical Feature Extraction
  for i in normalized_gsr:
    working_data, measures = statistical_feature_extraction(i, sample_rate)
    for k in measures.keys():
        s_measures = append_dict(s_measures, k, measures[k])
    for k in working_data.keys():
        s_working_data = append_dict(s_working_data, k, working_data[k])

  wd = s_working_data
  m = s_measures
  
  
  # Deep Learning Feature Extraction
  ###
  ### Your code here
  ###
  
  ############################ Feature Extraction Part ############################
  #################################################################################
  
  
  
  
  ##########################################################################################
  ############################ Visualizing Statistical Features ############################
  
  # Mapping the indexlist of each window to original data: comment it if you do not use windowing
  for index,i2 in enumerate(wd['indexlist']):
    for index2,j2 in enumerate(i2):
      wd['indexlist'][index][index2] = j2+segment_width*sample_rate*index

  # Storing the peaks for visualization
  peaks = []
  for index,i2 in enumerate(wd['indexlist']):
    for index2,j2 in enumerate(i2):
      peaks.append(j2)

  # Visualize the data with detected peaks marked with "x"
  ng = normalization(rolling_mean(data, 1./sample_rate, sample_rate))
  plt.plot(ng)
  plt.plot(peaks, ng[peaks], "x")
  plt.show()

  print(m['mean_gsr'])
  print(m['number_of_peaks'])
  print(m['max_of_peaks'])
  
  ############################ Visualizing Statistical Features ############################
  ##########################################################################################
  
  
  
  
  ###############################################################################################
  ############################ Creating train data with their labels ############################

  # Creating input X for classifier
  for i2 in range(0, len(wd['segment_indices'])):
    tmp = [m['mean_gsr'][i2],m['max_of_peaks'][i2],m['number_of_peaks'][i2]]
    X.append(tmp)
    # Based on their label from your data set: here is just set as i
    Y.append(i2)

  Xtrain = np.array(X)
  Ytrain = np.array(Y)
  
  ############################ Creating train data with their labels ############################
  ###############################################################################################
  
  
  
######################################################################## 
############################ Classification ############################
'''
You Need to update this part completely based on your data set.
'''

'''
# Select which classifier you want to use
knn = False
naiveBayes = False
rndForest = False
svm = False

# Creating empty Dictionaries for accuracies and predictions
Accuracy = {}
Predictions = {}

if (knn):
  knnLearner,_ = knnClassifier(Xtrain, Ytrain, K=range(1,3))
  YtestHat = knnLearner.predict(Xtest)
  Accuracy['knn'] = accuracy_score(Ytest, YtestHat)
  Predictions['knn'] = YtestHat
if (naiveBayes):
  naiveBayesLearner,_ = NaiveBayesGaussianClassifier(Xtrain, Ytrain)
  YtestHat = naiveBayesLearner.predict(Xtest)
  Accuracy['naiveBayes'] = accuracy_score(Ytest, YtestHat)
  Predictions['naiveBayes'] = YtestHat
if (rndForest):
  rndForestLearner,_ = RandomForestClassifier(Xtrain, Ytrain, D=range(1,3))
  YtestHat = rndForestLearner.predict(Xtest)
  Accuracy['rndForest'] = accuracy_score(Ytest, YtestHat)
  Predictions['rndForest'] = YtestHat
if (svm):
  svmLearner,_ = SVMClassifier(Xtrain, Ytrain)
  YtestHat = svmLearner.predict(Xtest)
  Accuracy['svm'] = accuracy_score(Ytest, YtestHat)
  Predictions['svm'] = YtestHat

Predictions['size'] = len(Ytest)

TournamentSelection(Accuracy, Predictions)
'''

############################ Classification ############################
########################################################################