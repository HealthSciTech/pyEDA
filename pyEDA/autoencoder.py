import torch
import numpy as np
from torch import nn
import math


class AE(nn.Module):
    def __init__(self, **kwargs):
        super().__init__()
        closest_pow2 = pow(2,int(math.floor(math.log(kwargs["input_shape"],2))))
		
		# Encoder layers
        self.linear1 = nn.Linear(in_features=kwargs["input_shape"], out_features=closest_pow2)
        self.conv1 = nn.Conv1d(1, 64, 3, padding=1)
        self.conv2 = nn.Conv1d(64, 32, 3, padding=1)
        self.conv3 = nn.Conv1d(32, 16, 3, padding=1)
        self.maxpool = nn.MaxPool1d(2, 2)
        self.linear2 = nn.Linear(in_features=(closest_pow2)*2, out_features=kwargs["latent_size"])
		
		# Decoder layers
        self.linear3 = nn.Linear(in_features=kwargs["latent_size"], out_features=(closest_pow2)*2)
        self.deconv1 = nn.ConvTranspose1d(16, 32, 2, stride=2)
        self.deconv2 = nn.ConvTranspose1d(32, 64, 2, stride=2)
        self.deconv3 = nn.ConvTranspose1d(64, 1, 2, stride=2)
        self.linear4 = nn.Linear(in_features=closest_pow2, out_features=kwargs["input_shape"])
		
        
    def forward(self, features):
		# Encoder
        activation = self.linear1(features)
        activation = torch.reshape(activation, (activation.shape[0],1,activation.shape[1]))
        activation = self.conv1(activation)
        activation = torch.relu(activation)
        activation = self.maxpool(activation)
        activation = self.conv2(activation)
        activation = torch.relu(activation)
        activation = self.maxpool(activation)
        activation = self.conv3(activation)
        activation = torch.relu(activation)
        activation = self.maxpool(activation)
        d = activation.shape
        activation = torch.reshape(activation, (d[0],d[1]*d[2]))
        code = self.linear2(activation)

		# Decoder
        activation = self.linear3(code)
        activation = torch.reshape(activation, (d[0],d[1],d[2]))
        activation = self.deconv1(activation)
        activation = torch.relu(activation)
        activation = self.deconv2(activation)
        activation = torch.relu(activation)
        activation = self.deconv3(activation)
        activation = torch.sigmoid(activation)
        activation = torch.reshape(activation, (activation.shape[0],activation.shape[2]))
        reconstructed = self.linear4(activation)
		
        return reconstructed, code
		

def create_train_loader(gsrData, batch_size=10):
	train_loader = []
	tensor_data = []
	
	for data in gsrData:
		tensor_data.append(np.array(data).flatten())
		if (len(tensor_data) == batch_size):
			train_loader.append(tensor_data)
			tensor_data = []

	if (len(tensor_data) != 0):
		print("Train data concatenated due to incompatible batch_size!")
	
	return torch.FloatTensor(train_loader)