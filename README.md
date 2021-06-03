# pyEDA
This is pyEDA v.2.0.
<br />This package includes all you need for Electrodermal Activity analysis also known as GSR. It contains preprocessing of the EDA signal and its feature extraction. Features are extracted using statistical and automatic methods.
<br />Convolutional autoencoder is used to extract the automatic featues.

# Data Collection
All the plots and the data collected for this package are collected from Shimmer GSR+ wearable sensor with 128 Hz frequency sampling rate. 

# How to use?
After cloning the repository to your local directory use the following command to import the library in your code:
```
from pyEDA.main import *
```
# Extract Statistical Features
Use the following command in your code to analysis the data:
```
m, wd, eda_clean = process_statistical(eda, use_scipy=True, sample_rate=128, new_sample_rate=40, segment_width=600, segment_overlap=0)
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
<br />
<b>eda_clean:</b> preprocessed gsr data

# Extract Automatic Features
Use the following command in your code to train the autoencoder:
```
prepare_automatic(eda_signals, sample_rate=128, new_sample_rate=40, k=32, epochs=100, batch_size=10)
```
<b>inputs::</b>
<br />
<b>eda_signals:</b> All eda signals (must be normalized to 0-1 range since the activation function of last layer is sigmoid.) targeted for feature extraction (2d list: nxm, n=number of signals, m=length of each signal)
<br />
<b>sample_rate:</b> sample rate which the data is collected at
<br />
<b>new_sample_rate:</b> new sample rate to downsample the data to
<br />
<b>epochs:</b> the number of epochs to train the autoencoder
<br />
<b>k:</b> the number of automatic features to extract
<br />
<b>batch_size:</b> the batch size to train the autoencoder
<br />

After the autoencoder is trained and saved, use the following command in your code to extract the automatic features:
```
automatic_features = process_automatic(eda)
```
<b>inputs::</b>
<br />
<b>eda:</b> the GSR signal
<br />
<b>returns::</b>
<br />
<b>automatic_features:</b> extracted automatic features
<br />

# Documentation
Here you can find the link to different notebooks about all the aspects of analysis of the GSR signal. These documentations include information about preprocessing and feature extraction of EDA signal.
<br />
<br />
These show how to handle various analysis tasks with pyEDA, from a random generated GSR data.
<br />
<br />
Here you can find the list of notebooks for feature extraction of EDA signal:
* [Statistical Feature Extraction](documentations/GSRStatFeatureExtraction/GSRStatFeatureExtraction.ipynb), a notebook explaining statistical feature extraction of GSR signal.
  
* [Automatic Feature Extraction](documentations/GSRAutoFeatureExtraction/GSRAutoFeatureExtraction.ipynb), a notebook explaining automatic feature extraction of GSR using an autoencoder.

# Citation
```
pyEDA: An Open-Source Python Toolkit for Pre-processing and Feature Extraction of Electrodermal Activity
```
```
Full bibtex reference:

@article{aqajari2021pyeda,
  title={pyEDA: An Open-Source Python Toolkit for Pre-processing and Feature Extraction of Electrodermal Activity},
  author={Aqajari, Seyed Amir Hossein and Naeini, Emad Kasaeyan and Mehrabadi, Milad Asgari and Labbaf, Sina and Dutt, Nikil and Rahmani, Amir M},
  journal={Procedia Computer Science},
  volume={184},
  pages={99--106},
  year={2021},
  publisher={Elsevier}
}
```
