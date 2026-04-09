import boto3

ec2 = boto3.resource('ec2')

def monitorear_instancias():
    print(f"{'ID Instancia':<20} | {'Estado':<12} | {'Tipo':<12} | {'IP Pública'}")
    print("-" * 70)
    
    for instancia in ec2.instances.all():
        ip = instancia.public_ip_address if instancia.public_ip_address else "N/A"
        print(f"{instancia.id:<20} | {instancia.state['Name']:<12} | {instancia.instance_type:<12} | {ip}")

monitorear_instancias()