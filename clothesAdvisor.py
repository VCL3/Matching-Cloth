import cv2
import numpy
from newConx import *
from defClothes import *


class ANN(BackpropNetwork):
	"""
	A specialied backprop network for classifying face images for
	the position of head.
	"""
	def classify(self, output):
		"""
		This ensures that that output layer is the correct size for this
		task, and then tests whether the output value is within
		tolerance of 1 (meaning sunglasses are present) or 0 (meaning
		they are not).
		"""
		assert(len(output) == len(article_text))
		maxOutput = max(output)
		return article_text[output.index(maxOutput)]


	def getOutput(self):
		"""
		For the current set of inputs, tests each one in the network to
		determine its classification, compares this classification to
		the targets, and computes the percent correct.
		"""
		if len(self.inputs) == 0:
			print 'no patterns to evaluate'
			return

		for i in range(len(self.inputs)):
			pattern = self.inputs[i]
			output = self.propagate(input=pattern)
			return self.classify(output)




class ClothesAdvisor:
	def __init__(self, verbose=0):
		self.weights = "ANN/final"
		self.ANN = self.establishANN()
		# self.KColors = 

		self.PHist = []


		self.verbose = verbose

	def establishANN(self):
		n = ANN()
		n.addLayers(w * h * 4, len(article_text) *2, len(article_text)) 
		# w, h, article_text defined in defClothes.py
		# set the training parameters
		n.setEpsilon(0.3)
		n.setMomentum(0.1)
		n.setReportRate(1)
		n.setTolerance(0.2)
		n.loadWeightsFromFile(self.weights)
		return n

	def evaluateClothes(self, imageAddress):
		category = self.getClothesCategory(imageAddress)
		print category




	def getClothesCategory(self, imageAddress, inputFile = "inputs/tem.dat"):
		self.getInput(imageAddress, inputFile)
		self.ANN.loadInputsFromFile(inputFile)
		return self.ANN.getOutput()


	def getInput(self, imageAddress, inputFile):
		infile = open(inputFile, "w")
		image_rgb = cv2.imread(imageAddress)
		cv2.imshow("c", image_rgb)
		cv2.waitKey(0)
		image_rgb = cv2.resize(image_rgb, (w,h), image_rgb, 0, 0, cv2.INTER_LANCZOS4)
		edges = cv2.Canny(image_rgb, 100, 200)

		for x in range(image_rgb.shape[0]):
			for y in range(image_rgb.shape[1]):
				isEdge = float(edges[x][y])/255.0
				infile.write("%.4f " % isEdge)
				for c in range(image_rgb.shape[2]):
					color = float(image_rgb[x][y][c])/255.0
					infile.write("%.4f " % color)
		infile.close()


advisor = ClothesAdvisor()
advisor.evaluateClothes('img/lg-1116.jpg')