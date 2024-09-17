import boto3

# Usar el perfil DevOps configurado en AWS CLI
session = boto3.Session(profile_name='devops')
s3 = session.resource('s3')

# Listar todos los buckets S3
for bucket in s3.buckets.all():
    print(bucket.name)
