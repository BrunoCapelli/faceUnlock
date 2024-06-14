import requests

def LoginStepOne(url, idDevice, hwdId):

	params = {
		'idDevice': idDevice,
		'hwd': hwdId
	}
	request = requests.post(url, params=params, verify=False)
	return request.content

def LoginStepTwo(url, idUser, idDevice, hwdId, token):
	headers = {'Authorization': f'Bearer {token}'}
	params = {
		'idDevice': idDevice,
		'idUser': idUser,
		'hwd': hwdId
	}
	request = requests.post(url, params=params, headers=headers, verify=False)
	return request