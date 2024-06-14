import os
import requests
import json
from modules import hardwareModule, apiModule, faceAuthModule

dataPath = 'C:/Users/bruno/OneDrive/Desktop/TakeControl_faceUnlock/Data' # Main route
imagePaths = os.listdir(dataPath)
#print('imagePaths=',imagePaths)



def main():

	urlDevice = 'https://localhost:44305/api/Device/LoginStepOne'
	urlUser = 'https://localhost:44305/api/User/LoginStepTwo'
	hwd = hardwareModule.getHardwareID()

	retries = 0
	isUserDetected = False

	#  Get access token 
	response = apiModule.LoginStepOne(urlDevice, 1, 'hwd')
	response_dict = json.loads(response)
	access_token = response_dict['accessToken']


	while retries <= 2 and not isUserDetected:
		isUserDetected = faceAuthModule.LBPHFaceDetection()
		if(isUserDetected):
			isUserDetected = True
		else:
			retries+=1

	if(isUserDetected):
		try:
			responseLogin = apiModule.LoginStepTwo(urlUser, 'Bruno', 1, 'hwd', access_token)
			#print(responseLogin.status_code)
		except Exception as e:
			print(e)
	else:
		try:
			request = requests.post(urlUser, params={
				'idDevice': 2,
				'idUser': 'unknown',
				'hwd': 'null'}, verify=False)
			print(request)
		except Exception as e:
			print(e) 

if __name__ == "__main__":
    main()


