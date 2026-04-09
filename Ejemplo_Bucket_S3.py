import boto3

# Creamos un cliente para el servicio S3
s3 = boto3.client('s3')

# Llamamos a una función para listar buckets
response = s3.list_buckets()

print("Tus cubetas disponibles:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")