from platform import release
from tkinter import font
import cv2, os, numpy as np

wajahDir = 'datawajah'
latihDir = 'latihwajah'

cam = cv2.VideoCapture(0)
#cam.set = (3, 640) #lebar camera
#cam.set = (4, 480) #tinggi camera

#klik link lalu copy paste ke note pad save as sbg html lalu load
#https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

#membaca data dari file yang telah di training
faceRecognizer.read(latihDir+'/training.xml')
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

id = 0
names = ['Tidak Diketahui', 'Tampan dan Berani', 'Tampan dan berani 2']

minWidht = 0.1*cam.get(3)
minHeight = 0.1*cam.get(4)

while True : #fungsi untuk pengulangan
    retV, frame = cam.read()
    frame = cv2.flip(frame, 1) #vertical flip
    abuabu = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuabu, 1.2, 5,minSize=(round(minWidht),round(minHeight)),) #frame, scalefactor, ninNeighbor
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        id, confidence = faceRecognizer.predict(abuabu[y:y+h,x:x+w]) #confidence 0 artinya sempurna, persen kemiripan
        if confidence <=50 :
            nameID = names[id]
            confidenceTxt = "{0}%".format(round(100-confidence))
        else:
            nameID = names[0]
            confidenceTxt = "{0}%".format(round(100-confidence))
        cv2.putText(frame, str(nameID), (x+5, y-5),font,1,(255,255,255),2)
        cv2.putText(frame, str(confidenceTxt), (x+5, y+h-5),font,1,(255,255,0),1)
    cv2.imshow('Recognisi Wajah', frame)
    #cv2.imshow('Webcamku-Grey', abuabu)
    k = cv2.waitKey(1) & 0xFF 
    if k ==27 or k == ord('q') :
        break
print('Exit')    
cam.release()
cv2.destroyAllWindows()