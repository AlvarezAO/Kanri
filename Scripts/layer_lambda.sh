#!/bin/bash

# Variables del entorno
cd /home/alvaro/Proyectos/Kanri
sed -i 's/\r$//' .env
source .env

# Paso 1: Crear el directorio del layer y limpiar el anterior
echo "Creando directorio para las dependencias del layer..."
rm -rf $AWS_LAYER_DIR
mkdir -p $AWS_LAYER_DIR/python
echo "Directorio creado en: $(readlink -f $AWS_LAYER_DIR)"

# Paso 2: Instalar las dependencias en el directorio del layer
echo "Instalando dependencias en el directorio del layer..."
cd /home/alvaro/Proyectos/Kanri
pip install -r requirements.txt -t $AWS_LAYER_DIR/python
pip install --platform manylinux2010_x86_64 --implementation cp --only-binary=:all: --upgrade --target $AWS_LAYER_DIR/python #cryptography


# Paso 3: Crear un archivo ZIP del layer
echo "Creando archivo ZIP para el layer..."
cd $AWS_LAYER_DIR
zip -r9 ../kanri-layer.zip .
cd ..

# Paso 4: Subir el ZIP como una nueva versión del layer a Lambda
echo "Publicando el Layer en Lambda..."
LAYER_VERSION=$(aws lambda publish-layer-version \
  --layer-name $AWS_LAYER_NAME \
  --description "Librerías del proyecto Kanri" \
  --zip-file fileb://kanri-layer.zip \
  --compatible-runtimes python3.11 \
  --region $AWS_REGION \
  --output text --query Version)

echo "Layer publicado con la versión: $LAYER_VERSION"

# Paso 5: Asociar el nuevo Layer al Lambda
echo "Asociando el Layer al Lambda..."
aws lambda update-function-configuration \
  --function-name $AWS_LAMBDA_FUNCTION_NAME \
  --layers arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:layer:${AWS_LAYER_NAME}:${LAYER_VERSION} \
  --region $AWS_REGION

echo "Layer asociado exitosamente al Lambda."

# Paso 6: Eliminar el directorio temporal del layer y el archivo ZIP
echo "Eliminando archivos temporales..."
rm -rf $AWS_LAYER_DIR kanri-layer.zip

echo "Espacio liberado y proceso completado."
