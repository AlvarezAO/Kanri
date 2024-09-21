import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, text
import json


#Usar AWS SECRET mas adelante, por ahora en desarrollo no es necesario
def get_secret():
    secret_name = "rds!db-09ba5175-7829-4458-896b-d4b2926463aa"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret


'''SECRET = get_secret()
HOST_RDS = "kanri-database.cxmiiiegiwuu.us-east-1.rds.amazonaws.com"
USER_RDS = SECRET['username']
PASS_RDS = SECRET['password']
DB_NAME_RDS = "kanri_desarrollo"'''

HOST_RDS = "konning.cpoks2q4o10c.us-east-1.rds.amazonaws.com"
USER_RDS = "admin"
PASS_RDS = "198711*_Aa"
DB_NAME_RDS = "kanri_desarrollo"

DATABASE_URL = f"mysql+pymysql://{USER_RDS}:{PASS_RDS}@{HOST_RDS}/{DB_NAME_RDS}?charset=utf8mb4"

print(DATABASE_URL)
# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)


def test_connection():
    """Intenta realizar una consulta simple para probar la conexión a la base de datos."""
    try:
        with engine.connect() as connection:
            # Ejecutar una consulta simple para probar la conexión
            result = connection.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result]

            if tables:
                print("Conexión exitosa. Las tablas en la base de datos son:")
                for table in tables:
                    print(table)
            else:
                print("Conexión exitosa, pero no se encontraron tablas.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")


if __name__ == "__main__":
    test_connection()
