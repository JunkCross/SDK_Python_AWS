# SDK_Python_AWS

Este repositorio contiene una serie de ejercicios prácticos para aprender a usar el SDK de AWS (boto3) con Python. Cada ejercicio demuestra diferentes funcionalidades de AWS, como S3, EC2, CloudWatch, IAM, etc. Estos scripts están diseñados para principiantes que quieren aprender a integrar aplicaciones Python con servicios de AWS.

## Requisitos Previos

- Python 3.x instalado
- Cuenta de AWS con credenciales configuradas (usando AWS CLI o variables de entorno)
- Instalar boto3: `pip install boto3`
- Permisos adecuados en AWS para los servicios utilizados

## Ejercicios

### 1. Ejercicio1_S3.py - Operaciones Básicas con S3
Demuestra cómo crear un bucket S3, subir un archivo, listar objetos y descargar archivos. Incluye manejo de errores y creación automática de buckets si no existen.

### 2. Ejercicio2_Backup_S3.py - Backup de Archivos a S3
Script para respaldar una carpeta local a un bucket S3, organizando los archivos por fecha en una estructura de carpetas.

### 3. Ejercicio3_monitor_EC2.py - Monitoreo de Instancias EC2
Monitorea el estado de instancias EC2, mostrando información como estado, tipo, zona de disponibilidad, etc.

### 4. Ejercicio4_Limpiador_S3.py - Limpieza de Buckets S3
Script para eliminar objetos antiguos o no deseados de un bucket S3, útil para mantenimiento.

### 5. Ejercicio5_CloudWatch.py - Métricas con CloudWatch
Ejemplo de cómo obtener métricas de CloudWatch para monitorear recursos de AWS.

### 6. Ejercicio6_Usuarios_IAM.py - Gestión de Usuarios IAM
Demuestra operaciones básicas con usuarios de IAM: listar, crear y gestionar usuarios.

### 7. Ejercicio7_Inventario_JSON.py - Inventario de Recursos en JSON
Genera un inventario de recursos AWS en formato JSON, útil para auditorías o reportes.

## Cómo Ejecutar

1. Clona el repositorio: `git clone <url>`
2. Instala dependencias: `pip install boto3`
3. Configura tus credenciales AWS
4. Ejecuta cualquier script: `python Ejercicio1_S3.py`

## Aprendizaje

Estos ejercicios cubren conceptos fundamentales de AWS SDK:
- Configuración de clientes y recursos
- Manejo de excepciones
- Operaciones CRUD en diferentes servicios
- Buenas prácticas de seguridad
