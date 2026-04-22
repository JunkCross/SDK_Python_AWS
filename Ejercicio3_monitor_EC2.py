"""
Ejercicio 3: Monitoreo y Creación de Instancias EC2

Este script demuestra cómo:
- Crear instancias EC2 con configuración personalizada
- Listar todas las instancias en tu cuenta
- Mostrar información relevante como estado, tipo y nombre

Aprende sobre recursos EC2, tags y manejo de instancias.
"""

import boto3
from botocore.exceptions import ClientError

# Inicializar el recurso EC2
# Asegúrate de que tu sesión de AWS esté activa (especialmente si usas AWS Academy/LabRole)
ec2 = boto3.resource('ec2')

def crear_instancia_personalizada():
    """
    Crea una nueva instancia EC2 t3.micro con Amazon Linux 2023.

    Solicita el nombre de la instancia al usuario y la etiqueta apropiadamente.

    Returns:
        str: ID de la instancia creada, o None si falla
    """
    try:
        # 1. Solicitar el nombre por terminal
        nombre_instancia = input("Ingresa el nombre para tu instancia (Tag Name): ")

        print(f"\nSolicitando creación de instancia t3.micro...")

        # 2. Crear la instancia con tus especificaciones exactas
        instancias = ec2.create_instances(
            # Amazon Linux 2023 AMI (x86_64) - Verifica que esta AMI esté disponible en tu región
            ImageId='ami-0a914de4dc1f18727',
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            # Aplicar el nombre mediante Tags
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': nombre_instancia},
                    ]
                },
            ]
        )

        nueva_instancia = instancias[0]
        print(f"✓ Instancia creada exitosamente.")
        print(f"  ID: {nueva_instancia.id}")
        print(f"  Tipo: {nueva_instancia.instance_type}")

        return nueva_instancia.id

    except ClientError as e:
        # Captura errores específicos de AWS (permisos, límites de cuenta, etc.)
        print(f"✗ Error de AWS: {e.response['Error']['Message']}")
    except Exception as e:
        # Captura cualquier otro error de Python
        print(f"✗ Ocurrió un error inesperado: {e}")

def listar_y_monitorear():
    """
    Lista todas las instancias EC2 en la cuenta actual.

    Muestra ID, estado, tipo de instancia y nombre (de tags).
    """
    print(f"\n{'ID Instancia':<20} | {'Estado':<12} | {'Tipo':<10} | {'Nombre'}")
    print("-" * 70)

    try:
        for instancia in ec2.instances.all():
            # Extraer el nombre de los Tags si existe
            nombre = "N/A"
            if instancia.tags:
                for tag in instancia.tags:
                    if tag['Key'] == 'Name':
                        nombre = tag['Value']

            print(f"{instancia.id:<20} | {instancia.state['Name']:<12} | {instancia.instance_type:<10} | {nombre}")
    except Exception as e:
        print(f"Error al listar: {e}")

# Ejecución del programa
if __name__ == "__main__":
    crear_instancia_personalizada()
    listar_y_monitorear()