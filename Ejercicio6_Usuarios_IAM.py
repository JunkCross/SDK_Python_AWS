"""
Ejercicio 6: Creación y Gestión de Usuarios IAM

Este script demuestra cómo crear un usuario en AWS Identity and Access Management (IAM),
asignarle una política de permisos predefinida y generar credenciales de acceso (Access Keys).

Funcionalidades:
- Crear un nuevo usuario IAM
- Adjuntar una política de solo lectura para S3
- Generar y mostrar las Access Keys del usuario

Requisitos:
- Credenciales AWS con permisos para gestionar IAM
- Permisos para crear usuarios, adjuntar políticas y generar keys

Advertencia:
- Las Access Keys generadas se muestran en la consola. En producción, usa métodos seguros
  para manejar credenciales (ej. AWS Secrets Manager).
- Recuerda rotar las keys regularmente y eliminar usuarios no utilizados.

Uso:
- Ejecutar el script para crear un usuario de ejemplo.
"""

import boto3
import json

# Inicialización del cliente IAM
iam = boto3.client('iam')


def crear_usuario_iam(nombre_usuario):
    """
    Crea un nuevo usuario IAM, le asigna una política de solo lectura para S3 y genera Access Keys.

    Args:
        nombre_usuario (str): Nombre del usuario IAM a crear.

    Returns:
        dict or None: Diccionario con las credenciales del usuario creado, o None si falla.

    Raises:
        ClientError: Si hay errores en las operaciones de IAM.
    """
    try:
        # Crear el usuario IAM
        iam.create_user(UserName=nombre_usuario)
        print(f"Usuario '{nombre_usuario}' creado exitosamente en IAM.")

        # Adjuntar política de solo lectura para Amazon S3
        iam.attach_user_policy(
            UserName=nombre_usuario,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
        )
        print(f"Política 'AmazonS3ReadOnlyAccess' adjuntada al usuario '{nombre_usuario}'.")

        # Generar Access Keys para el usuario
        keys = iam.create_access_key(UserName=nombre_usuario)

        # Preparar las credenciales en un diccionario
        creds = {
            "User": nombre_usuario,
            "AccessKey": keys['AccessKey']['AccessKeyId'],
            "SecretKey": keys['AccessKey']['SecretAccessKey']
        }

        print(f"Access Keys generadas para el usuario '{nombre_usuario}'.")
        return creds

    except iam.exceptions.EntityAlreadyExistsException:
        print(f"El usuario '{nombre_usuario}' ya existe en IAM.")
        return None
    except Exception as e:
        print(f"Error creando el usuario IAM: {e}")
        return None


if __name__ == "__main__":
    # Crear un usuario de ejemplo
    nombre_usuario_ejemplo = 'desarrollador_junior'
    nuevo_user = crear_usuario_iam(nombre_usuario_ejemplo)

    # Mostrar las credenciales si se crearon exitosamente
    if nuevo_user:
        print("\nCredenciales del nuevo usuario:")
        print(json.dumps(nuevo_user, indent=4))
    else:
        print("No se pudieron crear las credenciales del usuario.")