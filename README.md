# pyEDA
This is pyEDA v.1.2.
<br />This package includes all you need for Electrodermal Activity analysis also known as GSR. It contains preprocessing of the EDA signal and its feature extraction. (Features are extracted using statistical algorithms and deep learning)
<br />
<br />
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
Use the following command in your code to analysis the data:
```
m, wd = process(eda, use_scipy=True, sample_rate=128, new_sample_rate=40, segment_width=600, segment_overlap=0)
```
<b>inputs::</b>
<br />
<b>eda:</b> the GSR signal
<br />
<b>use_scipy:</b> set true to use scipy for peak extraction from phasic gsr (recommended)
<br />
<b>sample_rate:</b> sample rate which the data is collected at
<br />
<b>new_sample_rate:</b> new sample rate to downsample the data to
<br />
<b>segment_width:</b> segmentation of signal in seconds
<br />
<b>segment_overlap:</b> overlap of segments in seconds
<br />
<br />
<b>returns::</b>
<br />
<b>m:</b> all the measurements of the signals for each of the segment indices (number of peaks, mean of EDA, maximum value of the peaks)
<br />
<b>wd:</b> filtered phasic gsr, phasic gsr, tonic gsr, and peacklist for each of the segment indices

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
# Citation
```
GSR Analysis for Stress: Development and Validation of an Open Source Tool for Noisy Naturalistic GSR Data
```
```
Full bibtex reference:

@article{aqajari2020gsr,
  title={GSR Analysis for Stress: Development and Validation of an Open Source Tool for Noisy Naturalistic GSR Data},
  author={Aqajari, Seyed Amir Hossein and Naeini, Emad Kasaeyan and Mehrabadi, Milad Asgari and Labbaf, Sina and Rahmani, Amir M and Dutt, Nikil},
  journal={arXiv preprint arXiv:2005.01834},
  year={2020}
}
```
