from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

from utils.generator import generate_examples

import h5py
import datetime
import os
import pygame
from Controller import *
from Data import *
from Pygame_UI import *
from rover import Rover
import cv2
import numpy as np
import time
import sys
import scipy.misc

def convert(image):
    converted_img = image
    converted_img = np.mean(converted_img,2)
    converted_img = converted_img[100:228,0:330]
    converted_img = scipy.misc.imresize(converted_img,[128,128])
    converted_img = np.expand_dims(converted_img,3)
    return converted_img

if __name__ == '__main__':
	f = h5py.File('onehot_dataset.h5','r')
	dx = f['x_dataset']
	dy = f['y_dataset']
	
	actual_img = dx[0]
	actual_ang = dy[0]

	network = input_data(shape=[None, 128, 128, 1])
	network = conv_2d(network, 96, 11, strides=4, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 256, 5, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 3, activation='softmax')
	network = regression(network, optimizer='momentum',
	                     loss='categorical_crossentropy',
	                     learning_rate=0.001)

	#self.model = Evaluator(self.network, model='model_alexnet_rover-7400') #FIXME: path just a placeholder
	model = tflearn.DNN(network)
	model.load(os.getcwd() + '/weights/ALexVINN_model_Feb4.tfl')

	converted = convert(actual_img)
	cvt = np.array([converted])
	print(model.predict(cvt))
	print("Correct answer:", actual_ang)












