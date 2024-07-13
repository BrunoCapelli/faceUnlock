from modules import faceAuthModule


def register():
    
    user_name = input("Ingrese el nombre del usuario a registrar: ")
    try:
        faceAuthModule.Generate_Faces(user_name)
        faceAuthModule.Training_Model(user_name)
    except Exception as e:
        print(e)



""" if __name__ == "register": """
register()