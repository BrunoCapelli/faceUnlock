import cv2, imutils, hashlib


def LBPHFaceDetection():

	# Create the LBPHFace Recognizer
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Read the model
	face_recognizer.read('./models/modelLBPHF_test0106.xml')	

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
				label, confidence = face_recognizer.predict(face)
				result_str = f"Label: {label}, Confidence: {confidence}"
				hash_object = hashlib.sha256(result_str.encode())
				hex_dig = hash_object.hexdigest() # Get the hash on hex format

				print(f'El hash generado es {hex_dig} ')

				 

				if result[1] < 70:
					counter = counter + 2
					
					if(counter > 30):
						# Case where the person was detected. At least 15 frames had matched with the person's face
						print('Known user detected')
						isRunning = False
						isRecognized = True

						cap.release()
						cv2.destroyAllWindows()
				else:
					counter -= 1
					if (counter <= 0):
						# Case where the person was not detected. None of the frames contained the person face
						cap.release()
						cv2.destroyAllWindows()
			#cv2.imshow('FaceAuth',frame)
	cap.release()  # This line is to stop the input
	cv2.destroyAllWindows()
	
	return isRecognized