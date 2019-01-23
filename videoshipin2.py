import cv2
import numpy as np
c=1
timeF = 10 
cap = cv2.VideoCapture(0)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if(c%timeF == 0):
        cv2.imwrite('image/'+str(c) + '.jpg',frame)
        cv2.imshow("capture2", frame)
    c = c + 1
cap.release()
cv2.destroyAllWindows() 
