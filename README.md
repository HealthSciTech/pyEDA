# pyEDA
This is pyEDA v.1.1.
<br />This package includes all you need for Electrodermal Activity analysis also known as GSR. It contains preprocessing of the EDA signal and its feature extraction.
<br />pyEDA v1.1. supports classification at the end of the pipeline. 
<br />Classification, and tournament_selection folders are added to this version. You can find more information about the classification part at the end of this readme on Classification section.

# Data collection
All the plots and the data collected for this package are comming from Shimmer GSR+ wearable sensor. If you are using other sensors to collect EDA signal, you may need to use your own openShimmerFile.py based on your file. Otherwise, you can use openShimmerFile.py with minor changes. 

# How to use?
Use the following command to clone the repository to your local directory:
```
git clone https://github.com/AmirAJ95/pyEDA/
```
Go to the git directory and use the following command to analyze the data: 
```
python pyEDA/pyEDA/main.py
```
NOTE: make sure you are using the correct directory for your file.
<br />
NOTE: default version of pipeline does not use any classifier, for using classifier update the determined commented parts of classifier in main.py based on your data set.

# Documentation
Here you can find the link to different notebooks about all the aspects of analysis of the GSR signal. These documentations include information about preprocessing and feature extraction of EDA signal.
<br />
<br />
These show how to handle various analysis tasks with pyEDA, from noisy data collected from Shimmer GSR+.
<br />
<br />
Here you can find the list of notebooks starting from preprocessing of EDA signal to extracting its features.
* [GSR preprocessing](documentations/GSRPreprocessing/GSR_Preprocessing.ipynb), a notebook explaining preprocessing part of GSR.
  * Downsampling
  * Moving Window Averaging
  * Normalization
  * Extracting tonic and phasic components of signal using cvxPDA.py.
  * Butterworth Low pass filter
* [GSR feature extraction](documentations/GSRFeatureExtraction/GSR_Feature_Extraction.ipynb), a notebook explaining feature extraction of GSR.
  * Number of peaks
  * Maximum value of GSR
  * Mean value of GSR

# Classification
There are some commented parts in the main.py about classification that you need to update them based your data set. (The way you like to put your data, labels, etc.)
<br /><br />
This version of pipeline currently includes k-nearest neighbour classifier, naive bayes gaussian classifier, random forest classifier, and svm classifier. You can select your desired classifiers by setting their value to True in main.py.
<br /><br />
At the end of the pipeline we use simple ensemble method to produce the final prediction on the test data. We have TournamentSelection which calculates the weighted average predictions of all of your selected classifiers where the weight is the accuracy of each classifier on the test data.
