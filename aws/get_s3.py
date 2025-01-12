import boto3

# Usar el perfil DevOps configurado en AWS CLI
session = boto3.Session(profile_name='develop')
s3 = session.resource('s3')

# Listar todos los buckets S3
for bucket in s3.buckets.all():
    print(bucket.name)

# Configurar API Gateway client
client = session.client('apigateway', region_name='us-east-1')

# Obtener APIs existentes en API Gateway

response = client.get_rest_apis()
print(response['items'])

