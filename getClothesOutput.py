import cv2
import numpy


def getTarget(targetFile, imageFilenameRoot, inputFile, outputFile):

	target = open(targetFile, "r")
	outfile = open(outputFile, "w")
	infile = open(inputFile, "w")

	i = 1
	while 1:
		line = target.readline().split()
		if len(line) == 0: break
		if line[1] == "Suit":
			outfile.write("1\n")
		else:
			outfile.write("0\n")
		image = cv2.imread(imageFilenameRoot + line[0]+".jpg")
		h = 14
		w = 11

		smallImg = numpy.empty((h,w), 'uint8')
		image = cv2.resize(image, (w,h), smallImg, 0, 0, cv2.INTER_LANCZOS4)
		smallImg = smallImg.astype(float)
		smallGray = numpy.empty((h,w), 'uint8')
		cv2.cvtColor(image, cv2.COLOR_RGB2GRAY, smallGray)
		smallImg = numpy.divide(smallGray*1.0, 255.0)
		for row in smallImg:
			for col in row:
				infile.write("%.4f " % col)
		infile.write("\n")

		# numpy.savetxt(inputFile, smallImg, fmt="%.4f")
		# if i:
		# 	# cv2.imshow('Image', numpy.multiply(smallImg,255))
		# 	# while cv2.waitKey(15) < 0: pass
		# 	break

		# print smallImg.shape




	target.close()
	outfile.close()
	infile.close()

getTarget("clothes.dat", "img/lg-", "clothes-input.dat", "clothes-targets.dat")