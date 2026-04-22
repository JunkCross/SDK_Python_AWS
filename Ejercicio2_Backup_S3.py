"""
Ejercicio 2: Backup Automático de Archivos a S3

Este script demuestra cómo realizar backups automáticos de una carpeta local
a un bucket de Amazon S3, organizando los archivos por fecha.

Características:
- Recorre recursivamente una carpeta local
- Sube archivos a S3 con estructura organizada por fecha
- Útil para backups periódicos de fotos, documentos, etc.
"""

import boto3
import os
from datetime import datetime

# Configuración - Cambia estos valores según tu necesidad
s3 = boto3.resource('s3')
bucket_name = 'alan670265371833'  # Reemplaza con tu bucket
ruta_local = './mi_carpeta_fotos'  # Carpeta a respaldar

def backup_a_s3():
    """
    Realiza el backup de todos los archivos en la carpeta local a S3.

    Organiza los archivos en una estructura jerárquica por fecha:
    backups/YYYY-MM-DD/nombre_archivo
    """
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    bucket = s3.Bucket(bucket_name)

    print(f"Iniciando backup de '{ruta_local}' a S3...")

    for raiz, dirs, archivos in os.walk(ruta_local):
        for nombre_archivo in archivos:
            ruta_completa = os.path.join(raiz, nombre_archivo)
            # Estructura: backups/YYYY-MM-DD/archivo.jpg
            clave_s3 = f"backups/{fecha_hoy}/{nombre_archivo}"

            try:
                bucket.upload_file(ruta_completa, clave_s3)
                print(f"✓ Respaldado: {clave_s3}")
            except Exception as e:
                print(f"✗ Error respaldando {nombre_archivo}: {e}")

    print("Backup completado.")

if __name__ == "__main__":
    backup_a_s3()