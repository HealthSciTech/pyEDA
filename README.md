# pyEDA
This is pyEDA v.1.0.
<br />This package includes all you need for Electrodermal Activity analysis also known as GSR. It contains preprocessing of the EDA signal and its feature extraction.

# Data collection
All the plots and the data collected for this package are collected from Shimmer GSR+ wearable sensor. If you are using other sensors to collect EDA signal, you may need to use your own openShimmerFile.py based on your file. Otherwise, you can use openShimmerFile.py with minor changes. 

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
