# Kanri Project - Setup and Deployment

Proyecto Kanri, software para servicio tecnico


## 1. Requisitos Previos:
- **AWS CLI**: Configurada en tu máquina con las credenciales necesarias.
- **Python 3.11**: Instalado y configurado en tu entorno.
- **Virtualenv**: Para manejar las dependencias.
- **pip**: Administrador de paquetes Python.

### AWS Resources:
- VPC con subred pública y privada configurada.
- Instancia EC2 para conectar al RDS.
- Base de datos MySQL en RDS.

## 2. Clonar el Proyecto:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Kanri
```

## 3. Configuración del Entorno Virtual:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Despliegue de Código y Dependencias:

### Lambda:
- Subir el código del proyecto a Lambda utilizando GitHub Actions configurado en el repositorio.

### Layer de Lambda:
- Ejecutar el script para empaquetar dependencias y subir el Layer de Lambda.
- Asegúrate de que todas las dependencias están en el archivo `requirements.txt`.

```bash
./layer_lambda.sh
```

## 5. Configuración de API Gateway:
Para desplegar nuevas APIs en API Gateway o actualizar las existentes, ejecuta:

```bash
./deploy_api.sh <code_id> <entorno>
```
- **code_id**: El identificador único para la API.
- **entorno**: Puede ser development, staging o production.

## 6. Configuración de la EC2 para Conectar a RDS:

### SSH Tunnel:
Usa un túnel SSH para conectar a RDS desde tu máquina local.

```bash
ssh -i <PEM_FILE> -L 3306:<RDS_ENDPOINT>:3306 ec2-user@<EC2_PUBLIC_IP>
```

Luego, desde herramientas como DataGrip o DBeaver, puedes conectar a tu RDS a través de la IP local.

## 7. Administración de Costos:
- Recuerda detener la instancia EC2 cuando no la utilices.
- Configura una alarma de costos en AWS para evitar sorpresas al final del mes.

## 8. Ejecutar y Probar APIs:
- Todas las rutas de las APIs pueden probarse directamente en API Gateway o mediante herramientas como Postman.
