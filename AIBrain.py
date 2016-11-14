# -*- coding: utf-8 -*-

""" AlexNet.
Applying 'Alexnet' to Oxford's 17 Category Flower Dataset classification task.
References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
    - 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.
Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
    - [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
"""
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

from rover import Rover
from Pygame_UI import *
import numpy as np
import pygame
import cv2
import time
import math

#load the data
X = np.load("dataset/img.npy")
Y = np.load("dataset/ang.npy")

X = X / 255

Y= (Y - 90)/90

class AIBrain(Rover):
	def __init__(self):
		Rover.__init__(self)
		self.fname = 'racetrackrover.model'

		self.model = self.alexNetModel()
		self.model = self.loadModel(self.fname)

		self.displayUI = Pygame_UI()
		self.angle = None
		self.quit = False
		self.image = None
		self.clock = pygame.time.Clock()
		self.FPS = 30
		self.treads = [0,0]
		self.runAI()

	def runAI(self):
		print(self.get_battery_percentage())
		oldTreads = None
		newTime = time.time()
		while not self.quit:
			for event in pygame.event.get():
				if event.type ==pygame.QUIT:
					self.quit == True
				if event.type == pygame.KEYDOWN:
					if event.key == "Q":
						self.quit == True
			self.angle = self.getAngle(self.image)
			# self.useButtons()
			self.getNewTreads()
			newTreads = self.treads
			# self.process_video_from_rover()
			oldTime = time.time()
			timer = abs(newTime - oldTime)
			if oldTreads != newTreads:
				self.freeze()
			if oldTreads != newTreads or timer > 1:
				newTime = time.time()
				oldTreads = newTreads
				self.set_wheel_treads(newTreads[0], newTreads[1])
			cv2.imshow("RoverCam", self.image)
			self.imgAngle = self.displayWithAngle(self.angle, self.image)
			cv2.imshow("Display Angle", self.imgAngle)
			self.imgEdges = self.edges(self.image)
			cv2.imshow("RoverCamEdges", self.imgEdges)

			self.clock.tick(self.FPS)
			self.displayUI.screen.fill((255,255,255))
		self.endSession()

	def getAngle(self):
		angle = self.model.predict([self.image])
		# FIXME: probably not right
		angle = (90 * angle) + 90  # converts tanh (-1,1) to 0-180 range??
		return angle

	def getNewTreads(self):
			if self.angle <= 180 and self.angle >= 130:
				self.treads = [-1,1]
			elif self.angle < 130 and self.angle >= 100:
				self.treads = [-0.05, 1] #0,1
			elif self.angle < 100 and self.angle >= 80:
				self.treads = [1, 1]
			elif self.angle < 80 and self.angle >= 50:
				self.treads = [1, -0.05] #1,0
			elif self.angle < 50 and self.angle >= 0:
				self.treads = [1,-1]

	def freeze(self):
		self.treads = [0, 0]
		self.set_wheel_treads(0, 0)

	def endSession(self):
		self.set_wheel_treads(0,0)
		pygame.quit()
		cv2.destroyAllWindows()

	def process_video_from_rover(self, jpegbytes, timestamp_10msec):
		window_name = 'Machine Perception and Cognitive Robotics'
		array_of_bytes = np.fromstring(jpegbytes, np.uint8)
		self.image = cv2.imdecode(array_of_bytes, flags=3)
		k = cv2.waitKey(5) & 0xFF
		return self.image


	def displayWithAngle(self, angle, frame):
		imgAngle = frame.copy()
		if self.angle and not self.isReversed:
			radius = 80
			angle = angle * math.pi / 180
			y = 240 - int(math.sin(angle) * radius)
			x = int(math.cos(angle) * radius) + 160
			# cv2.circle(frame, (160, 240), radius, (250, 250, 250), -1)
			cv2.line(imgAngle, (160, 240), (x, y), (0, 0, 0), 5)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(imgAngle, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2)
		return imgAngle

	def alexNetModel(self):
		# Building 'AlexNet'
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
		network = fully_connected(network, 4096, activation='tanh')
		network = dropout(network, 0.5)
		network = fully_connected(network, 4096, activation='tanh')
		network = dropout(network, 0.5)
		network = fully_connected(network, 1, activation='tanh')
		network = regression(network, optimizer='momentum',
							 loss='categorical_crossentropy',
							 learning_rate=0.001)

		# Training
		model = tflearn.DNN(network, checkpoint_path='model_rtr', max_checkpoints=1, tensorboard_verbose=2)
		return model

	def fitModel(self, model):
		model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
				  show_metric=True, batch_size=64, snapshot_step=200,
		snapshot_epoch=False, run_id='model_racetrackrover')
		return model

	def loadModel(self, model,fname):
		model.load(fname)
		return model

	def saveModel(self, model, fname):
		model.save(fname)
		return model

AI = AIBrain()