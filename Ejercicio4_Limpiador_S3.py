import boto3
from datetime import datetime, timedelta, timezone

s3 = boto3.resource('s3')
bucket_name = 'alan670265371833'

def limpiar_bucket():
    bucket = s3.Bucket(bucket_name)
    limite = datetime.now(timezone.utc) - timedelta(days=30)
    
    for objeto in bucket.objects.all():
        if objeto.last_modified < limite:
            print(f"Eliminando {objeto.key} (Antigüedad: {objeto.last_modified})")
            objeto.delete()

limpiar_bucket()