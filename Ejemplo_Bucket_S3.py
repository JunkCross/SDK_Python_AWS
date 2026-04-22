"""
Ejemplo Básico: Listado de Buckets S3

Este script demuestra el uso básico del SDK de AWS para Python (boto3) para interactuar con Amazon S3.
Lista todos los buckets S3 disponibles en la cuenta configurada.

Funcionalidades:
- Conectar a S3 usando boto3
- Listar y mostrar los nombres de todos los buckets

Requisitos:
- Credenciales AWS configuradas (aws configure)
- Permisos para listar buckets S3

Uso:
- Ejecutar el script para ver los buckets disponibles en tu cuenta.
"""

import boto3


def listar_buckets_s3():
    """
    Lista y muestra todos los buckets S3 en la cuenta AWS actual.

    Returns:
        None

    Raises:
        ClientError: Si hay errores accediendo a S3.
    """
    try:
        # Crear cliente para el servicio S3
        s3 = boto3.client('s3')

        # Obtener la lista de buckets
        response = s3.list_buckets()

        # Mostrar los buckets disponibles
        print("Tus buckets S3 disponibles:")
        if response['Buckets']:
            for bucket in response['Buckets']:
                print(f"- {bucket['Name']}")
        else:
            print("No se encontraron buckets en tu cuenta.")

    except Exception as e:
        print(f"Error listando buckets S3: {e}")


if __name__ == "__main__":
    # Ejecutar el listado de buckets
    listar_buckets_s3()