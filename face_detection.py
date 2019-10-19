import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cv2.namedWindow('Webcam')
cap = cv2.VideoCapture(0)
if (cap.isOpened()):
    ret = True
else:
    ret = False

while (ret):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Chuyển thành màu trắng đen để xử lý nhanh hơn vì
    # Vì ảnh trắng đen chỉ có 1 kênh màu
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # Xác định khuôn mặt
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        # Vẽ một hình chữ nhật bao quanh tọa độ khuôn mặt được xác định
        
        roi_gray = gray[y:y+h, x:x+w] # Lấy một ROI của ảnh trắng đen để xác định mắt
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray) # Xác định mắt
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2) 
             # Vẽ một hình chữ nhật bao quanh tọa độ mắt được xác định
            
    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1)
    if key == 27: # Chương trình sẽ dừng nếu bấm esc
        break

cap.release()
cv2.destroyAllWindows()