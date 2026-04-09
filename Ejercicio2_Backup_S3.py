import boto3
import os
from datetime import datetime

s3 = boto3.resource('s3')
bucket_name = 'alan670265371833'
ruta_local = './mi_carpeta_fotos' # Carpeta a respaldar

def backup_a_s3():
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    bucket = s3.Bucket(bucket_name)

    for raiz, dirs, archivos in os.walk(ruta_local):
        for nombre_archivo in archivos:
            ruta_completa = os.path.join(raiz, nombre_archivo)
            # Estructura: backup/2026-04-08/archivo.jpg
            clave_s3 = f"backups/{fecha_hoy}/{nombre_archivo}"
            
            bucket.upload_file(ruta_completa, clave_s3)
            print(f"Respaldado: {clave_s3}")

backup_a_s3()