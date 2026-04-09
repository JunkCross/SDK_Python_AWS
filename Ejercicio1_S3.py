import boto3
import os
from botocore.exceptions import ClientError

# Configuración del cliente
s3 = boto3.client('s3')

def obtener_ruta_local(nombre_archivo):
    # Obtiene la ruta del directorio donde se encuentra este script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio_actual, nombre_archivo)

def asegurar_bucket():
    # Obtenemos la región configurada en tu cliente/entorno
    region_actual = s3.meta.region_name
    
    while True:
        nombre_bucket = input("\nIngresa el nombre del bucket de S3: ").strip()
        
        try:
            s3.head_bucket(Bucket=nombre_bucket)
            print(f"El bucket '{nombre_bucket}' ya existe y tienes acceso.")
            return nombre_bucket
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == '404':
                print(f"El bucket '{nombre_bucket}' no existe en {region_actual}. Intentando crearlo...")
                try:
                    # Si la región es us-east-1, no se debe pasar CreateBucketConfiguration
                    if region_actual == 'us-east-1':
                        s3.create_bucket(Bucket=nombre_bucket)
                    else:
                        # Para cualquier otra región, este bloque es OBLIGATORIO
                        s3.create_bucket(
                            Bucket=nombre_bucket,
                            CreateBucketConfiguration={
                                'LocationConstraint': region_actual
                            }
                        )
                    print(f"Bucket '{nombre_bucket}' creado exitosamente en {region_actual}.")
                    return nombre_bucket
                except Exception as ex:
                    print(f"No se pudo crear el bucket: {ex}. Intenta con otro nombre.")
            else:
                print(f"Error de permisos o nombre inválido ({error_code}). Reintenta.")

def s3_operations():
    # 1. Asegurar que el bucket exista
    bucket_name = asegurar_bucket()
    
    # Definimos los nombres de los archivos
    nombre_archivo_subida = 'archivo_local.txt'
    ruta_completa_subida = obtener_ruta_local(nombre_archivo_subida)
    
    # Crear un archivo de prueba si no existe en la ruta del script
    if not os.path.exists(ruta_completa_subida):
        with open(ruta_completa_subida, 'w') as f:
            f.write("Contenido de prueba para S3")

    try:
        # 2. Subir archivo desde la ruta del script
        print(f"\nSubiendo {nombre_archivo_subida} desde {ruta_completa_subida}...")
        s3.upload_file(ruta_completa_subida, bucket_name, 'remoto.txt')
        print("Subida exitosa.")

        # 3. Listar archivos
        print("\nArchivos actualmente en el bucket:")
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print("El bucket está vacío.")

        # 4. Descargar archivo a la ruta del script
        ruta_descarga = obtener_ruta_local('descargado_de_s3.txt')
        s3.download_file(bucket_name, 'remoto.txt', ruta_descarga)
        print(f"\nDescarga exitosa. Archivo guardado en: {ruta_descarga}")
        
    except ClientError as e:
        print(f"Ocurrió un error durante las operaciones de S3: {e}")

if __name__ == "__main__":
    s3_operations()