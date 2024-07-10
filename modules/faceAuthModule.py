import cv2, imutils, hashlib, os, numpy as np
from modules import paths 


def LBPHFaceDetection():

	# Create the LBPHFace Recognizer
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Read the model
	face_recognizer.read('./models/modelLBPHF_test0106.xml')	

	# Inputs
	#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	#cap = cv2.VideoCapture('C:/Users/bruno/OneDrive/Desktop/faceUnlock/test/test3.mp4')
	cap = cv2.VideoCapture(0)

	#faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
	cascade_filename = '/home/admin/takeControl/TakeControlDevice/haarcascade_frontalface_default.xml'
	cascade_path = os.path.join(os.path.dirname(cv2.__file__), 'takeControl', cascade_filename)
	faceClassif = cv2.CascadeClassifier(cascade_path)


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

				#print(f'El hash generado es {hex_dig} ')
				print(counter)

				 

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


def Generate_Faces(userName):
    
	personName = userName
	dataPath = paths.DATA
	personPath = os.path.join(dataPath, userName)

	if not os.path.exists(personPath):
		print('Folder created: ',personPath)
		os.makedirs(personPath)
	
	#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Debug pictures on live camera
	#cap = cv2.VideoCapture('C:/Users/bruno/OneDrive/Desktop/faceUnlock/test/vid01.mp4') # Analyze frame by frame from video
	#cap = cv2.VideoCapture('/home/admin/takeControl/TakeControlDevice/vid01.mp4') # Analyze frame by frame from video
	cap = cv2.VideoCapture(0)

	#faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

	cascade_filename = '/home/admin/takeControl/TakeControlDevice/haarcascade_frontalface_default.xml'
	cascade_path = os.path.join(os.path.dirname(cv2.__file__), 'takeControl', cascade_filename)
	faceClassif = cv2.CascadeClassifier(cascade_path)

	count = 0
	isRunning = True

	while isRunning:
		ret, frame = cap.read() 
		if ret == False: break
		frame =  imutils.resize(frame, width=640)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = frame.copy()
		faces = faceClassif.detectMultiScale(gray,1.3,5)
		for (x,y,w,h) in faces:
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
			face = auxFrame[y:y+h,x:x+w]
			face = cv2.resize(face,(150,150),interpolation=cv2.INTER_CUBIC)
			cv2.imwrite(personPath + '/_face_{}.jpg'.format(count),face)
			count = count + 1
			print(count)
			if(count == 250):
				isRunning = False
			
		#cv2.imshow('frame',frame)

		k =  cv2.waitKey(1)
		if k == 27 or count >= 450:
			break

	cap.release()
	cv2.destroyAllWindows()

def Training_Model(modelName):
    dataPath = paths.DATA
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

    face_recognizer.write(modelName+'.xml')
    print("Model created!")