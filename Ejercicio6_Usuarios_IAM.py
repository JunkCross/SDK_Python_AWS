import boto3
import json

iam = boto3.client('iam')

def crear_usuario_iam(nombre_usuario):
    try:
        # Crear usuario
        iam.create_user(UserName=nombre_usuario)
        
        # Asignar política de solo lectura (ejemplo)
        iam.attach_user_policy(
            UserName=nombre_usuario,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
        )
        
        # Generar llaves
        keys = iam.create_access_key(UserName=nombre_usuario)
        
        creds = {
            "User": nombre_usuario,
            "AccessKey": keys['AccessKey']['AccessKeyId'],
            "SecretKey": keys['AccessKey']['SecretAccessKey']
        }
        
        print(f"Usuario {nombre_usuario} creado con éxito.")
        return creds
        
    except iam.exceptions.EntityAlreadyExistsException:
        print("El usuario ya existe.")

nuevo_user = crear_usuario_iam('desarrollador_junior')
print(json.dumps(nuevo_user, indent=4))