#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time
import pandas as pd

import caffe


def main(input_file):
	print(input_file)
	pycaffe_dir = os.path.dirname(__file__)
	print(pycaffe_dir)

	model_def = os.path.join(pycaffe_dir,
				"network/foodclassify.prototxt")
	pretrained_model = os.path.join(pycaffe_dir,
				"model/mobilenet.caffemodel")
	image_dims = [224, 224]
	mean = np.load(os.path.join(pycaffe_dir, 'ilsvrc_2012_mean.npy')).mean(1).mean(1)
	channel_swap = [2, 1, 0]
	input_scale = None
	raw_scale = 255.0
	labels_file = os.path.join(pycaffe_dir,
				"foodnames.txt")

	caffe.set_mode_cpu()

	# Make classifier.
	classifier = caffe.Classifier(model_def, pretrained_model,
			image_dims=image_dims, mean=mean,
			input_scale=input_scale, raw_scale=raw_scale,
			channel_swap=channel_swap)

	# Load numpy array (.npy), directory glob (*.jpg), or image file.
	#print(input_file)
	input_file = os.path.expanduser(input_file[-1])
	if input_file.endswith('npy'):
		print("Loading file: %s" % input_file)
		inputs = np.load(args.input_file)
	elif os.path.isdir(input_file):
		print("Loading folder: %s" % input_file)
		inputs =[caffe.io.load_image(im_f)
				 for im_f in glob.glob(input_file + '/*.' + args.ext)]
	else:
		print("Loading file: %s" % input_file)
		inputs = [caffe.io.load_image(input_file)]

	print("Classifying %d inputs." % len(inputs))

	# Classify.
	start = time.time()
	print("INPUTS")
	print(inputs)
	scores = classifier.predict(inputs, True).flatten()
	print("Done in %.2f s." % (time.time() - start))
	

	#Print Results
	with open(labels_file) as f:
		labels_df = pd.DataFrame([
		   {
			   'id': int(l.strip().split(' ')[0]),
			   'foodname': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
		   }
		   for l in f.readlines()
		])

	labels = labels_df.sort_values('id')['foodname']

	indices = (-scores).argsort()[:5]
	predictions = labels[indices]

	meta = [
	   (p, float(scores[i]))
	   for i, p in zip(indices, predictions)
	   ]

	return meta

if __name__ == '__main__':
	print(sys.argv)
	main(sys.argv)
