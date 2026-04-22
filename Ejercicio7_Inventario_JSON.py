"""
Ejercicio 7: Generación de Inventario de Recursos AWS en JSON

Este script genera un inventario completo de recursos AWS clave y lo guarda en un archivo JSON.
Recopila información sobre instancias EC2, buckets S3 y funciones Lambda en la cuenta actual.

Funcionalidades:
- Listar todas las instancias EC2 activas
- Listar todos los buckets S3
- Listar todas las funciones Lambda
- Guardar el inventario en 'aws_inventory.json'

Requisitos:
- Credenciales AWS configuradas con permisos para EC2, S3 y Lambda
- Permisos de solo lectura para los servicios mencionados

Uso:
- Ejecutar el script para generar el inventario.
- Revisar el archivo 'aws_inventory.json' generado.

Nota:
- Este script asume que tienes acceso a los recursos en la región por defecto.
- Para múltiples regiones, modificar el código para iterar sobre regiones.
"""

import boto3
import json


def generar_inventario():
    """
    Genera un inventario de recursos AWS y lo guarda en un archivo JSON.

    Recopila IDs de instancias EC2, nombres de buckets S3 y nombres de funciones Lambda,
    organizándolos en un diccionario estructurado que se guarda como JSON.

    Returns:
        None

    Raises:
        ClientError: Si hay errores accediendo a los servicios AWS.
        IOError: Si hay problemas escribiendo el archivo JSON.
    """
    # Inicializar el diccionario del inventario
    inventario = {
        "ec2": [],
        "s3": [],
        "lambda": []
    }

    try:
        # Recopilar instancias EC2
        print("Recopilando instancias EC2...")
        ec2 = boto3.client('ec2')
        for reservation in ec2.describe_instances()['Reservations']:
            for instance in reservation['Instances']:
                inventario["ec2"].append(instance['InstanceId'])

        # Recopilar buckets S3
        print("Recopilando buckets S3...")
        s3 = boto3.client('s3')
        inventario["s3"] = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]

        # Recopilar funciones Lambda
        print("Recopilando funciones Lambda...")
        lam = boto3.client('lambda')
        for function in lam.list_functions()['Functions']:
            inventario["lambda"].append(function['FunctionName'])

        # Guardar el inventario en un archivo JSON
        with open('aws_inventory.json', 'w') as f:
            json.dump(inventario, f, indent=4)

        print("Inventario generado y guardado en 'aws_inventory.json'.")
        print(f"Recursos encontrados: EC2({len(inventario['ec2'])}), S3({len(inventario['s3'])}), Lambda({len(inventario['lambda'])})")

    except Exception as e:
        print(f"Error generando el inventario: {e}")


if __name__ == "__main__":
    # Ejecutar la generación del inventario
    generar_inventario()