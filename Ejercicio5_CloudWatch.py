import boto3
import random
from botocore.exceptions import ClientError

# Clientes
cw = boto3.client('cloudwatch')
sns = boto3.client('sns')

def configurar_sistema_alertas(email_contacto):
    try:
        # 1. Crear un Tópico de SNS (El medio de notificación)
        print("Configurando canal de notificación...")
        topic = sns.create_topic(Name='AlertasDeAplicacion')
        topic_arn = topic['TopicArn']

        # 2. Suscribir un correo (Nota: Debes confirmar el mail que te llegue)
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_contacto
        )
        print(f"Suscripción enviada a {email_contacto}. Revisa tu bandeja de entrada.")

        # 3. Crear la Alarma en CloudWatch
        # Si la métrica 'ErroresCriticos' es mayor a 5 en 1 minuto, dispara la alarma.
        print("Creando alarma en CloudWatch...")
        cw.put_metric_alarm(
            AlarmName='Alarma_Errores_Script',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='ErroresCriticos',
            Namespace='SistemaMonitoreo/App',
            Period=60,
            Statistic='Sum',
            Threshold=5.0,
            ActionsEnabled=True,
            AlarmActions=[topic_arn],
            AlarmDescription='Alarma si el script detecta más de 5 errores por minuto',
            Dimensions=[{'Name': 'Modulo', 'Value': 'Procesamiento'}]
        )
        return topic_arn

    except ClientError as e:
        print(f"Error configurando el sistema: {e}")

def simular_actividad_con_metricas(topic_arn):
    # Simulamos que el script está corriendo y encuentra errores
    errores_detectados = random.randint(1, 10)
    
    print(f"Enviando métrica: {errores_detectados} errores detectados.")
    
    cw.put_metric_data(
        Namespace='SistemaMonitoreo/App',
        MetricData=[
            {
                'MetricName': 'ErroresCriticos',
                'Dimensions': [{'Name': 'Modulo', 'Value': 'Procesamiento'}],
                'Value': errores_detectados,
                'Unit': 'Count'
            },
        ]
    )
    
    if errores_detectados > 5:
        print("--- ALERTA: Umbral superado. CloudWatch activará la alarma pronto. ---")
    else:
        print("Estado normal.")

if __name__ == "__main__":
    # Cambia esto por tu correo para probar
    mi_correo = "tu_usuario@ejemplo.com" 
    
    arn_canal = configurar_sistema_alertas(mi_correo)
    
    if arn_canal:
        simular_actividad_con_metricas(arn_canal)