import cv2
import numpy as np

image = cv2.imread('res/opencv_logo.png')

cv2.namedWindow('window1')
cv2.imshow('window1', image)
cv2.waitKey(0) # tắt khi nhấn phím bất kì
cv2.destroyWindow('window1') # dọn dẹp tài nguyên