"""
Ejercicio 4: Limpieza Automática de Buckets S3

Este script elimina archivos antiguos de un bucket S3 basándose en la fecha
de última modificación. Útil para mantenimiento y reducción de costos.

Características:
- Elimina objetos con más de 30 días de antigüedad
- Muestra qué archivos se están eliminando
- Previene acumulación de archivos innecesarios
"""

import boto3
from datetime import datetime, timedelta, timezone

# Configuración
s3 = boto3.resource('s3')
bucket_name = 'alan670265371833'  # Reemplaza con tu bucket

def limpiar_bucket():
    """
    Elimina todos los objetos del bucket que tengan más de 30 días de antigüedad.

    Esto ayuda a mantener los buckets limpios y reduce costos de almacenamiento.
    """
    bucket = s3.Bucket(bucket_name)
    limite = datetime.now(timezone.utc) - timedelta(days=30)

    print(f"Limpiando bucket '{bucket_name}' - Eliminando archivos anteriores a {limite.date()}")

    objetos_eliminados = 0
    for objeto in bucket.objects.all():
        if objeto.last_modified < limite:
            print(f"  Eliminando: {objeto.key} (Modificado: {objeto.last_modified.date()})")
            objeto.delete()
            objetos_eliminados += 1

    print(f"\nLimpieza completada. {objetos_eliminados} objetos eliminados.")

if __name__ == "__main__":
    limpiar_bucket()