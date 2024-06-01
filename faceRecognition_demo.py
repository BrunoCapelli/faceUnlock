import cv2
import os
import imutils
import requests

dataPath = 'C:/Users/bruno/OneDrive/Desktop/TakeControl_faceUnlock/Data' # Main route
imagePaths = os.listdir(dataPath)
#print('imagePaths=',imagePaths)

def LBPHFaceDetection():

	# Create the LBPHFace Recognizer
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Read the model
	face_recognizer.read('modelLBPHF_test0106.xml')	

	# Inputs
	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	#cap = cv2.VideoCapture('C:/Users/bruno/OneDrive/Desktop/faceUnlock/test/test3.mp4')

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

	counter = 10
	isRecognized = False
	isRunning = True
	
	while isRunning:
		ret,frame = cap.read()
		if ret == False: 
			break
		else:
			frame =  imutils.resize(frame, width=640)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = faceClassif.detectMultiScale(gray,1.3,5)

			for (x,y,w,h) in faces:
				face = auxFrame[y:y+h,x:x+w]
				face = cv2.resize(face,(150,150),interpolation= cv2.INTER_CUBIC)
				result = face_recognizer.predict(face)
				#cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

				# LBPHFace
				if result[1] < 70:
					#cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					#cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
					counter = counter + 2
					
					if(counter > 30):
						# Case where the person was detected. At least 15 frames had matched with the person's face
						# Execute face auth
						print('Known user detected')
						isRunning = False
						isRecognized = True

						cap.release()
						cv2.destroyAllWindows()
				else:
					#cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					#cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
					counter -= 1
					if (counter <= 0):
						# Case where the person was not detected. None of the frames contained the person face
						cap.release()
						cv2.destroyAllWindows()
			# Show the input after processing it
			cv2.imshow('LBPHFace',frame)
	cap.release()  # This line is to stop the input
	cv2.destroyAllWindows()
	
	return isRecognized

### ### ### ### ### 

### Begins ###

url = 'https://localhost:44305/api/User/Login'
params = {
    'idDevice': 1,
    'idUser': 'Bruno',
    'hwd': 'hwd'
}
retries = 0
isUserDetected = False

while retries <= 2 and not isUserDetected:
	isUserDetected = LBPHFaceDetection()
	if(isUserDetected):
		isUserDetected = True
	else:
		retries+=1

if(isUserDetected):
	try:
		request = requests.post(url, params=params, verify=False)
		print(request)
	except Exception as e:
		print(e)
else:
	try:
		request = requests.post(url, params={
			'idDevice': 2,
			'idUser': 'unknown',
			'hwd': 'null'}, verify=False)
		print(request)
	except Exception as e:
		print(e)


