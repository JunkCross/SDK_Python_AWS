import boto3
import json

def generar_inventario():
    inventario = {
        "ec2": [],
        "s3": [],
        "lambda": []
    }

    # EC2
    ec2 = boto3.client('ec2')
    for inst in ec2.describe_instances()['Reservations']:
        for i in inst['Instances']:
            inventario["ec2"].append(i['InstanceId'])

    # S3
    s3 = boto3.client('s3')
    inventario["s3"] = [b['Name'] for b in s3.list_buckets()['Buckets']]

    # Lambda
    lam = boto3.client('lambda')
    for f in lam.list_functions()['Functions']:
        inventario["lambda"].append(f['FunctionName'])

    with open('aws_inventory.json', 'w') as f:
        json.dump(inventario, f, indent=4)
    
    print("Inventario guardado en aws_inventory.json")

generar_inventario()