import numpy
import cv2


cap = cv2.VideoCapture(0)

# win = 'Project 2'
# cv2.namedWindow(win)

while cv2.waitKey(15) < 0:
	ret, frame = cap.read()
	cv2.imshow('Project 2', frame)




