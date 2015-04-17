import cv2
import numpy


def getTarget(targetFile, imageFilenameRoot, inputFile, outputFile):

	target = open(targetFile, "r")
	outfile = open(outputFile, "w")
	infile = open(inputFile, "w")

	bottoms = ["trousers", "trouser", "jeans", "pants", "shorts", "sweatpants"]
	num_top = 0
	num_bottom = 0
	num_suit = 0
	i = 1
	max_num = 20
	while 1:
		isTop = True 

		line = target.readline().split()
		if len(line) == 0: break
		if "Suit" in line[1]:
			if num_suit >= max_num:
				continue
			outfile.write("1 0 0\n")
			isTop = False
			print "SUIT", line

			num_suit += 1

		for b in bottoms:
			if b == line[1].lower():
				if num_bottom >= max_num:
					continue
				outfile.write("0 1 0\n")
				print "BOTTOM", line
				line[1]
				isTop = False

				num_bottom += 1


		if isTop:
			if num_top >= max_num:
				continue

			outfile.write("0 0 1\n")
			print "TOP", line
			num_top += 1

		image = cv2.imread(imageFilenameRoot + line[0]+".jpg")
		# h = 144
		# w = 108
		h = 29
		w = 23

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


	print "All done", "top:", num_top, "bottoms:", num_bottom, "suits:", num_suit	

		# print smallImg.shape







	target.close()
	outfile.close()
	infile.close()

getTarget("clothes.dat", "img/lg-", "clothes-input.dat", "clothes-targets.dat")