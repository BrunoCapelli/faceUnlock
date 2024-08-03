import os
import requests
import json
from modules import hardwareModule, apiModule, faceAuthModule, paths, GPIO_handler
import time

dataPath = os.path.join(paths.MAIN_ROUTE, paths.DATA) # Main route
imagePaths = os.listdir(dataPath)
#print('imagePaths=',imagePaths)



def main():

	urlDevice = 'http://takecontrol.somee.com/api/Device/LoginStepOne'
	urlUser = 'http://takecontrol.somee.com/api/User/LoginStepTwo'
	hwd = hardwareModule.getHardwareID()

	retries = 0
	isUserDetected = False

	#  Get access token 
	response = apiModule.LoginStepOne(urlDevice, 1, 'hwd')
	print(response)
	response_dict = json.loads(response)
	access_token = response_dict['accessToken']


	while retries <= 2 and not isUserDetected:
		try:
			isUserDetected = faceAuthModule.LBPHFaceDetection()
			if(isUserDetected):
				isUserDetected = True
			else:
				retries+=1
		except Exception as e:
			print(e)

	if(isUserDetected):
		try:
			responseLogin = apiModule.LoginStepTwo(urlUser, 'Bruno', 1, 'hwd', access_token)
			print("Sending notification...")
			print(f"{responseLogin.request}   {responseLogin.content}")
			if responseLogin.ok:
				GPIO_handler.Activate_Pin17() # Green LED
				time.sleep(20)
		except Exception as e:
			print(e)
	else:
		try:
			request = apiModule.LoginStepTwo(urlUser, 'unknown', 2,'x',access_token)
			print(request)
			if request.ok:
				GPIO_handler.Activate_Pin27() # Red LED
				time.sleep(20)
		except Exception as e:
			print(e) 

if __name__ == "__main__":
	GPIO_handler.InitializePins()
	main()
	GPIO_handler.Deactivate()


