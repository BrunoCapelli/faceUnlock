
import cv2
import os
import numpy as np
from modules import paths

dataPath = paths.MAIN_ROUTE
peopleList = os.listdir(dataPath)

print('List of users: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print("Reading pictures...")

    for fileName in os.listdir(personPath):
        print('Rostros: ', nameDir + fileName )
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName, 0)) # Pic to gray scale

        image = cv2.imread(personPath+'/'+fileName, 0)
        #cv2.imshow('image',image) # Show pictures after applying gray scale
        #cv2.waitKey(10)
    label = label +1


face_recognizer = cv2.face.LBPHFaceRecognizer_create()

print("Trainning...")

face_recognizer.train(facesData, np.array(labels))

# Save the model

model_name=input("Ingrese un nombre de modelo: ")
face_recognizer.write(model_name+'.xml')
print("Model created!")
