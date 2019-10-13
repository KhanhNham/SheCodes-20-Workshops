import cv2
import numpy

video = cv2.VideoCapture(0) # Video source là video trong thư mục res

cv2.namedWindow('video')

while(video.isOpened()):
    ret, frame = video.read()
    if ret == False: # kiểm tra đã tới cuối video hay chưa
        break
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # Tắt video khi nhấn q
        break

video.release() # dọn dẹp tài nguyên
cv2.destroyAllWindows () # dọn dẹp tài nguyên