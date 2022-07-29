#pip install pillow

from platform import release
import PIL
import cv2, os, numpy as np
from PIL import Image

wajahdir = 'datawajah' #folder dir data wajah disimpan
latihDir = 'latihwajah' #folder data wajah akan disimpan
def getImageLabel(path): #pengambilan data wajah
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples = []
    faceids = []
    for imagePath in imagePaths:
        PILImg = Image.open(imagePath).convert('L') #convert ke dalam grey
        imgNum = np.array(PILImg, 'uint8')
        faceid = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = faceDetector.detectMultiScale(imgNum)
        for (x, y, w, h) in faces:
            faceSamples.append(imgNum[y:y+h,x:x+w])
            faceids.append(faceid)
        return faceSamples,faceid

faceRecognizer = cv2.face.LBPHFaceRecognizer_create() #package untuk algoritma facerecognize
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print('sedang berjalan')
faces,IDs = getImageLabel(wajahdir)
faceRecognizer.train(faces,np.array(IDs))

#simpan
faceRecognizer.write(latihDir+'/training.xml')
print('Sebanyak {0} data wajah telah dilatih ke main',format(len(np.unique(IDs))))

#jika berhasil akan ada file baru di folder latihwajah dengan format xml