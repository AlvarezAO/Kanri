#!/bin/bash

# Variables del entorno
API_NAME="Kanri"  # Nombre de la API en API Gateway
LAMBDA_FUNCTION_NAME="KanriLambda"
REGION="us-east-1"
CODE_ID=$1  # El primer argumento del script es el code_id
STAGE=$2   # El segundo argumento del script es el stage (ambiente: development, staging, production)

# Obtener el RestApiId de API Gateway usando el nombre de la API
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='${API_NAME}'].id" --output text --region ${REGION})
echo "API_ID: ${API_ID}"

# Llamar al script Python para obtener la ruta y el método basados en el code_id
ruta_info=$(python obtener_rutas.py $CODE_ID)

# Extraer el path y el method desde la salida del script Python
PATH_API=$(echo "$ruta_info" | jq -r '.path')
METHOD=$(echo "$ruta_info" | jq -r '.method')

# Comprobar si la API ya tiene la operación (code_id) registrada
EXISTING_OPERATION=$(aws apigateway get-resources --rest-api-id ${API_ID} --query "items[?path=='/${PATH_API}']" --output text --region ${REGION})

if [ -z "$EXISTING_OPERATION" ]; then
    echo "No existe la operación con el code_id ${CODE_ID}, se procederá a crearla..."

    # Crear la operación en la API
    PARENT_RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${API_ID} --query "items[?path=='/'].id" --output text --region ${REGION})

    RESOURCE_ID=$(aws apigateway create-resource --rest-api-id ${API_ID} --parent-id ${PARENT_RESOURCE_ID} --path-part ${CODE_ID} --query 'id' --output text --region ${REGION})

    # Vincular la operación a Lambda
    aws apigateway put-method --rest-api-id ${API_ID} --resource-id ${RESOURCE_ID} --http-method ${METHOD} --authorization-type "NONE" --region ${REGION}

    aws apigateway put-integration --rest-api-id ${API_ID} --resource-id ${RESOURCE_ID} --http-method ${METHOD} --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:YOUR_ACCOUNT_ID:function:${LAMBDA_FUNCTION_NAME}/invocations --region ${REGION}

    echo "Operación creada y vinculada a Lambda."
else
    echo "La operación ${CODE_ID} ya existe, no se realizará ningún cambio."
fi

# Implementar los cambios en la etapa correspondiente (stage)
aws apigateway create-deployment --rest-api-id ${API_ID} --stage-name ${STAGE} --region ${REGION}
echo "Despliegue realizado en el stage ${STAGE}."
