import torch
import numpy as np
from torch import nn


class AE(nn.Module):
    def __init__(self, **kwargs):
        super().__init__()
        self.encoder_hidden_layer_1 = nn.Linear(
            in_features=kwargs["input_shape"], out_features=128
        )
        self.encoder_hidden_layer_2 = nn.Linear(
            in_features=128, out_features=64
        )
        self.encoder_output_layer = nn.Linear(
            in_features=64, out_features=kwargs["latent_size"]
        )
        self.decoder_hidden_layer_1 = nn.Linear(
            in_features=kwargs["latent_size"], out_features=64
        )
        self.decoder_hidden_layer_2 = nn.Linear(
            in_features=64, out_features=128
        )
        self.decoder_output_layer = nn.Linear(
            in_features=128, out_features=kwargs["input_shape"]
        )

    def forward(self, features):
        activation = self.encoder_hidden_layer_1(features)
        activation = torch.relu(activation)
        activation = self.encoder_hidden_layer_2(activation)
        activation = torch.relu(activation)
        code = self.encoder_output_layer(activation)
        code = torch.relu(code)
        activation = self.decoder_hidden_layer_1(code)
        activation = torch.relu(activation)
        activation = self.decoder_hidden_layer_2(activation)
        activation = torch.relu(activation)
        activation = self.decoder_output_layer(activation)
        reconstructed = torch.relu(activation)
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