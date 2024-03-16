import cv2
import os
import imutils



dataPath = 'C:/Users/bruno/OneDrive/Desktop/faceUnlock/Data' # Main route
imagePaths = os.listdir(dataPath)
print('imagePaths=',imagePaths)

def LBPHFaceDetection():

	# Create the LBPHFace Recognizer
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Read the model
	face_recognizer.read('modelLBPHF_test1603.xml')	

	# Inputs
	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	#cap = cv2.VideoCapture('C:/Users/bruno/OneDrive/Desktop/faceUnlock/test/test3.mp4')

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

	counter = 10
	
	while True:
		ret,frame = cap.read()
		if ret == False: 
			print("Fail: The input is empty.")
			break

		frame =  imutils.resize(frame, width=640)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = gray.copy()

		faces = faceClassif.detectMultiScale(gray,1.3,5)
		print(counter)

		for (x,y,w,h) in faces:
			
			face = auxFrame[y:y+h,x:x+w]
			face = cv2.resize(face,(150,150),interpolation= cv2.INTER_CUBIC)
			result = face_recognizer.predict(face)

			cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

			# LBPHFace
			if result[1] < 70:
				cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				counter = counter + 2
				
				if(counter > 20):
					# Case where the person was detected. At least 10 frames had matched with the person's face
					# Execute face auth
					print('Known user detected')
					cap.release()
					cv2.destroyAllWindows()
				

			else:
				cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
				counter -= 1

				if (counter <= 0):
					# Case where the person was not detected. None of the frames contained the person face
					cap.release()
					cv2.destroyAllWindows()
				
			
		# Show the input after processing it
				
		cv2.imshow('LBPHFace',frame)
		#cv2.resizeWindow('frame', 800, 600)
		k = cv2.waitKey(1)
		if k == 27:
			break

	cap.release()  # This line is to stop the input
	cv2.destroyAllWindows()

### ### ### ### ### 

## Face Mesh ##
mp_face_mesh = mp.solutions.face_mesh

### Begins ###


LBPHFaceDetection()
print('milanesa')
#LBPHFaceDetection()



