import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.optimizers import SGD, Adam
import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def create_1Dcnn():
    model = models.Sequential()
    model.add(layers.Conv1D(filters=32, kernel_initializer='he_normal', kernel_size=3, activation='relu', input_shape=(60*20,1)))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv1D(filters=64, kernel_initializer='he_normal', kernel_size=3, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling1D(pool_size=2))
    model.add(layers.Flatten())
    model.add(layers.Dense(348, kernel_initializer='he_normal', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(2,activation='sigmoid'))
    myAdam = tf.keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=myAdam,
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy',sensitivity,specificity])
    return model

def deepFeatures(model):
    # feature extraction layer
    getFeature = K.function([model.layers[0].input, K.learning_phase()],
                            [model.layers[5].output])
    return getFeature

def deepPrediction(model):
    # classification layer
    getPrediction = K.function([model.layers[6].input, K.learning_phase()],
                               [model.layers[8].output])
    return getPrediction