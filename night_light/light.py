# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#  help="path to the image file")
# args = vars(ap.parse_args())
img = "/home/zq/work/yolov5/night_light/light.jpg"

#load the image, convert it to grayscale, and blur it
image = cv2.imread(img)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("/home/zq/work/yolov5/night_light/gray.png", gray)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
cv2.imwrite("/home/zq/work/yolov5/night_light/blurred.png", blurred)


# threshold the image to reveal light regions in the
# blurred image
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("./thresh.png", thresh)


# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image
thresh = cv2.erode(thresh, None, iterations=2)
cv2.imwrite("./erode.png", thresh)

thresh = cv2.dilate(thresh, None, iterations=4)
cv2.imwrite("./dilate.png", thresh)

# perform a connected component analysis on the thresholded
# image, then initialize a mask to store only the "large"
# components
labels = measure.label(thresh, neighbors=8, background=0)
cv2.imwrite("./labels.png", labels)

mask = np.zeros(thresh.shape, dtype="uint8")
# loop over the unique components
for label in np.unique(labels):
 # if this is the background label, ignore it
 if label == 0:
  continue
 # otherwise, construct the label mask and count the
 # number of pixels
 labelMask = np.zeros(thresh.shape, dtype="uint8")
 labelMask[labels == label] = 255
 numPixels = cv2.countNonZero(labelMask)
 # if the number of pixels in the component is sufficiently
 # large, then add it to our mask of "large blobs"
 if numPixels > 300:
  mask = cv2.add(mask, labelMask)