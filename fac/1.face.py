#pip install opencv-contrib-python

from platform import release
import cv2, os

wajahDir = 'datawajah'      #folder yang akan disimpan datanya
cam = cv2.VideoCapture(0)   #menjalankan camera webcam default webcam 0 sesuai yang terkonek
#cam.set = (3, 640) #lebar camera
#cam.set = (4, 480) #tinggi camera

#klik link lalu copy paste ke note pad save as sbg html lalu load
#https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
faceid = input('Masukan face id :') #menambahkan id untuk nama file
print ("Tatap wajah ke camera")
ambildata = 0
while True :        #fungsi untuk looping data
    retV, frame = cam.read()
    abuabu = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY) #convert ke abu2
    faces = faceDetector.detectMultiScale(abuabu, 1.3, 5) #frame, scalefactor, ninNeighbor
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2) #membuat kotak disekitar wajah
        namafile = 'wajah.'+str(faceid)+'.'+str(ambildata)+'.jpg' #membuat nama file yang akan disimpan
        cv2.imwrite(wajahDir+'/'+namafile, frame) #fungsi untuk membuat file
        ambildata += 1
        roiabuabu = abuabu[y:y+h,x:x+w]
        roiwarna = abuabu[y:y+h,x:x+w]
        eyes = eyeDetector.detectMultiScale(roiabuabu)
        for (xe, ye, we, he) in eyes:
            frame = cv2.rectangle(roiwarna, (xe,ye), (xe+we, ye+he), (0,0,255), 1)

    cv2.imshow('Webcamku', frame) #menampilkan webcam
    cv2.imshow('Webcamku-Grey', abuabu)
    k = cv2.waitKey(1) & 0xFF #perintah untuk berhenti
    if k ==27 or k == ord('q') :
        break
    elif ambildata >30:
        break
print('pengambilan data selesai')    
cam.release() #perintah untuk menghapus perintah open web
cv2.destroyAllWindows() #agar menghapus jendela open webcam

