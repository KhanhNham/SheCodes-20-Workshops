import cv2
import numpy as np

BLUE = [255,0,0]


# using imread to read image
img1 = cv2.imread('res/opencv_logo.png')

# replicate image 1
# The border will be replicated from the pixel values at the edges of the original image.
replicate = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REPLICATE)

# reflect image 1
reflect = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT)


reflect101 = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_WRAP)
constant= cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)

cv2.imshow('original', img1)

cv2.imshow('replicate', replicate)
cv2.imshow('reflect', reflect)

cv2.imshow('reflect101', reflect101)
cv2.imshow('wrap', wrap)
cv2.imshow('constant', constant)

cv2.waitKey(0)
cv2.destroyAllWindows()