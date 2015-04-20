import cv2
import numpy


def getTarget(targetFile, imageFilenameRoot, inputFile, outputFile):

	target = open(targetFile, "r")
	outfile = open(outputFile, "w")
	infile = open(inputFile, "w")

	tshirts = ["t-shirt", "poloshirt"]
	bottoms = ["trousers", "trouser", "jeans", "pants", "sweatpants", "jogger", "chino"]
	num_top = 0
	num_bottom = 0
	num_suit = 0
	num_shorts = 0
	num_tshirts = 0
	i = 20
	max_num = 40
	verbose = True
	while 1:
		isTop = True 

		line = target.readline().split()
		if len(line) == 0: break
		if "suit" in line[1].lower():
			if num_suit >= max_num:
				continue
			outfile.write("1 0 0 0 0\n")
			isTop = False
			if verbose:
				print "SUIT", line
			num_suit += 1

		if "shorts" == line[1].lower():
			if num_shorts >= max_num:
				continue
			outfile.write("0 0 0 1 0\n")
			isTop = False

			num_shorts += 1
			if verbose:
				print "SHORTS", line


		for t in tshirts:
			if t == line[1].lower():
				if num_tshirts >= max_num:
					continue
				outfile.write("0 1 0 0 0\n")
				isTop = False
				num_tshirts += 1
				if verbose:
					print "TSHIRT", line

		for b in bottoms:
			if b == line[1].lower():
				if num_bottom >= max_num:
					continue
				outfile.write("0 0 0 0 1\n")
				#print "BOTTOM", line
				isTop = False
				num_bottom += 1
				if verbose:
					print "BOTTOM", line


		if isTop:
			if num_top >= max_num:
				continue
			outfile.write("0 0 1 0 0\n")
			num_top += 1
			if verbose:
				print "TOP", line

		# read in image
		image_rgb = cv2.imread(imageFilenameRoot + line[0]+".jpg")

		# h = 144/2
		# w = 108/2
		h = 144/2
		w = 108/2

		# smallImg = numpy.empty((h,w), 'uint8')
		image_rgb = cv2.resize(image_rgb, (w,h), image_rgb, 0, 0, cv2.INTER_LANCZOS4)
		edges = cv2.Canny(image_rgb, 100, 200)

		# smallImg = smallImg.astype(float)
		# smallGray = numpy.empty((h,w), 'uint8')
		image = edges
		# cv2.cvtColor(image, cv2.COLOR_RGB2GRAY, smallGray)
		#smallImg = numpy.divide(smallGray*1.0, 255.0)

		for x in range(image.shape[0]):
			for y in range(image.shape[1]):
				pixel = float(image[x][y])/255.0
				# for c in range(image.shape[2]):
					# color = float(image[x][y][c])/255.0
					# if i:
					# 	print type(image[x][y][c])
					# 	print int(image[x][y][c])

					# 	i -= 1

				infile.write("%.4f " % pixel)
				
		infile.write("\n")

	print "All done", "top:", num_top, "tshirts", num_tshirts, "bottoms:", num_bottom, "suits:", num_suit, "shorts", num_shorts	

		# print smallImg.shape







	target.close()
	outfile.close()
	infile.close()

# getTarget("inputs/all.dat", "img/lg-", "inputs/tbs-30-144*108-color-input.dat", "inputs/tbs-30-144*108-color-targets.dat")
getTarget("inputs/all.dat", "img/lg-", "inputs/test-inputs.dat", "inputs/test-targets.dat")