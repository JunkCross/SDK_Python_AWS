"""
Ejercicio 5: Configuración de Alertas en CloudWatch con SNS

Este script demuestra cómo configurar un sistema de alertas en AWS utilizando CloudWatch y SNS.
Crea un tópico de SNS para notificaciones por email, configura una alarma en CloudWatch que se activa
cuando se detectan más de 5 errores críticos por minuto, y simula el envío de métricas para probar el sistema.

Requisitos:
- Credenciales AWS configuradas (aws configure)
- Permisos para CloudWatch, SNS y métricas personalizadas
- Un email válido para recibir notificaciones

Uso:
- Ejecutar el script para configurar el sistema y simular métricas.
"""

import boto3
import random
from botocore.exceptions import ClientError

# Inicialización de clientes AWS
cw = boto3.client('cloudwatch')
sns = boto3.client('sns')


def configurar_sistema_alertas(email_contacto):
    """
    Configura un sistema completo de alertas utilizando CloudWatch y SNS.

    Esta función crea un tópico de SNS para notificaciones, suscribe un email al tópico,
    y configura una alarma en CloudWatch que se activa cuando la métrica 'ErroresCriticos'
    supera el umbral de 5 errores por minuto.

    Args:
        email_contacto (str): Dirección de email para recibir notificaciones de alertas.

    Returns:
        str or None: ARN del tópico SNS creado, o None si ocurre un error.

    Raises:
        ClientError: Si hay errores en las llamadas a la API de AWS.
    """
    try:
        # Paso 1: Crear un Tópico de SNS para notificaciones
        print("Configurando canal de notificación...")
        topic = sns.create_topic(Name='AlertasDeAplicacion')
        topic_arn = topic['TopicArn']

        # Paso 2: Suscribir el email al tópico (requiere confirmación manual)
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_contacto
        )
        print(f"Suscripción enviada a {email_contacto}. Revisa tu bandeja de entrada y confirma la suscripción.")

        # Paso 3: Crear la Alarma en CloudWatch
        # La alarma se activa si 'ErroresCriticos' > 5 en 1 minuto
        print("Creando alarma en CloudWatch...")
        cw.put_metric_alarm(
            AlarmName='Alarma_Errores_Script',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='ErroresCriticos',
            Namespace='SistemaMonitoreo/App',
            Period=60,  # Período de evaluación en segundos
            Statistic='Sum',
            Threshold=5.0,
            ActionsEnabled=True,
            AlarmActions=[topic_arn],  # Acción: enviar notificación al tópico
            AlarmDescription='Alarma activada si el script detecta más de 5 errores críticos por minuto',
            Dimensions=[{'Name': 'Modulo', 'Value': 'Procesamiento'}]  # Dimensión para filtrar métricas
        )
        print("Sistema de alertas configurado exitosamente.")
        return topic_arn

    except ClientError as e:
        print(f"Error configurando el sistema de alertas: {e}")
        return None


def simular_actividad_con_metricas(topic_arn):
    """
    Simula la actividad de un script enviando métricas aleatorias a CloudWatch.

    Genera un número aleatorio de errores detectados (1-10), envía esta métrica a CloudWatch,
    y verifica si supera el umbral para activar la alarma.

    Args:
        topic_arn (str): ARN del tópico SNS (no utilizado en esta función, pero podría extenderse).

    Returns:
        None
    """
    # Simular errores detectados durante la ejecución del script
    errores_detectados = random.randint(1, 10)

    print(f"Enviando métrica a CloudWatch: {errores_detectados} errores críticos detectados.")

    # Enviar la métrica personalizada a CloudWatch
    cw.put_metric_data(
        Namespace='SistemaMonitoreo/App',
        MetricData=[
            {
                'MetricName': 'ErroresCriticos',
                'Dimensions': [{'Name': 'Modulo', 'Value': 'Procesamiento'}],
                'Value': errores_detectados,
                'Unit': 'Count'  # Unidad de medida: conteo
            },
        ]
    )

    # Verificar si se supera el umbral y mostrar mensaje correspondiente
    if errores_detectados > 5:
        print("--- ALERTA: Umbral superado. CloudWatch activará la alarma y enviará notificación por email. ---")
    else:
        print("Estado normal: Métrica dentro del rango aceptable.")


if __name__ == "__main__":
    # Configuración: Reemplaza con tu dirección de email real para recibir alertas
    mi_correo = "tu_usuario@ejemplo.com"

    # Configurar el sistema de alertas
    arn_canal = configurar_sistema_alertas(mi_correo)

    # Si la configuración fue exitosa, simular actividad y envío de métricas
    if arn_canal:
        simular_actividad_con_metricas(arn_canal)