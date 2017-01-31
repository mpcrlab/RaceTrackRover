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



if __name__ == '__main__':
	f = h5py.File('onehot_dataset.h5','r')
	dx = f['x_dataset']
	dy = f['y_dataset']
	
	actual_img = dx[0]
	actual_ang = dy[0]

	network = input_data(shape=[None, 240, 320, 3])
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
	network = fully_connected(network, 96, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 96, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 3, activation='softmax')
	network = regression(network, optimizer='momentum',
	                     loss='categorical_crossentropy',
	                     learning_rate=0.001)

	#self.model = Evaluator(self.network, model='model_alexnet_rover-7400') #FIXME: path just a placeholder
	model = tflearn.DNN(network)
	model.load('rovernet1_v2.tflearn')

	print("The model thinks this angle is correct:", model.predict(actual_img))
	print("The actual angle is:", actual_ang)












