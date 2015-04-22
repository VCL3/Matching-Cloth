import cv2
import numpy

#create a graphic window
win = 'Lines'
cv2.namedWindow(win)

image_rgb = cv2.imread('img/lg-1.jpg')
edges = cv2.Canny(image_rgb, 100, 200)
# lines = cv2.HoughLines(edges, 1, numpy.pi/180, 150)

cv2.imshow(win, image_rgb)
cv2.waitKey()
cv2.imshow(win, edges)
cv2.waitKey()