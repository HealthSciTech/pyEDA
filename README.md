# pyEDA
This is pyEDA v.1.1.
<br />This package includes all you need for Electrodermal Activity analysis also known as GSR. It contains preprocessing of the EDA signal and its feature extraction. (Features are extracted using statistical algorithms and deep learning)
NOTE: Deep learning feature extraction are under some changes. For now you can use the package for preprocessing and statistical features extraction.

# Data collection
All the plots and the data collected for this package are collected from Shimmer GSR+ wearable sensor with 128 Hz frequency sampling rate. 

# How to use?
Use the following command to clone the repository to your local directory:
```
git clone https://github.com/AmirAJ95/pyEDA/
```
Use the following command to import the library in your code:
```
from main import *
```
Use the following command to in your code to analysis the data:
```
m, wd = process(eda, sample_rate=128, new_sample_rate=40, segment_width=600, segment_overlap=0)
```
inputs::
eda: the GSR signal
sample_rate: sample rate which the data is collected at
new_sample_rate: new sample rate to downsample the data to
segment_width: segmentation of signal in seconds
segment_overlap: overlap of segments in seconds

returns::
m: all the measurements of the signals for each of the segment indices (number of peaks, mean of EDA, maximum value of the peaks)
wd: filtered phasic gsr, phasic gsr, tonic gsr, and peacklist for each of the segment indices

# Documentation
Here you can find the link to different notebooks about all the aspects of analysis of the GSR signal. These documentations include information about preprocessing and feature extraction of EDA signal. For windowing and segmentations, we use the same algorithm used in heartPy library.
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
