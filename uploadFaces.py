import cv2
import os
import imutils

try:
	personName = 'admin'
	dataPath = '/home/admin/takeControl/takeControl_data' 
	personPath = os.path.join(dataPath, personName)

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
except:
    print("error")