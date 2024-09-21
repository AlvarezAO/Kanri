#!/bin/bash

# Variables del entorno
API_NAME="Kanri"  # Nombre de la API en API Gateway
LAMBDA_FUNCTION_NAME="KanriLambda"
ACCOUNT_ID="982534361962"
REGION="us-east-1"
CODE_ID=$1  # El primer argumento del script es el code_id
STAGE=$2   # El segundo argumento del script es el stage (ambiente: development, staging, production)

# Obtener el RestApiId de API Gateway usando el nombre de la API
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='${API_NAME}'].id" --output text --region ${REGION})

# Llamar al script Python para obtener la ruta y el método basados en el code_id
ruta_info=$(python ./app/utils/deployments/find_paths.py $CODE_ID)
echo ${ruta_info} | jq

# Extraer el path y el method desde la salida del script Python
PATH_API=$(echo "$ruta_info" | jq -r '.path')
METHOD=$(echo "$ruta_info" | jq -r '.method')

# Función para obtener o crear resource ID de un path-part
get_or_create_resource_id() {
  PARENT_ID=$1
  PATH_PART=$2
  echo "Parent_id: ${PARENT_ID}" >&2
  echo "Path_part: ${PATH_PART}" >&2
  # Verificar si el recurso ya existe
  RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${API_ID} --query "items[?pathPart=='${PATH_PART}' && parentId=='${PARENT_ID}'].id" --output text --region ${REGION} --no-paginate)
  echo "RESOURCE_ID: ${RESOURCE_ID}" >&2
  if [ -z "$RESOURCE_ID" ]; then
    # Si no existe, crear el recurso
    RESOURCE_ID=$(aws apigateway create-resource --rest-api-id ${API_ID} --parent-id ${PARENT_ID} --path-part ${PATH_PART} --query 'id' --output text --region ${REGION} --no-paginate)
    echo "Recurso creado: ${PATH_PART} con ID: ${RESOURCE_ID}" >&2
  else
    echo "Recurso ya existente: ${PATH_PART} con ID: ${RESOURCE_ID}" >&2
  fi

  echo $RESOURCE_ID
}

# Obtener el recurso raíz
PARENT_RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${API_ID} --query "items[?path=='/'].id" --output text --region ${REGION} --no-paginate)

# Separar el path en partes y crear/verificar cada una
IFS='/' read -r -a PATH_PARTS <<< "$PATH_API"
for PART in "${PATH_PARTS[@]}"; do
  if [ ! -z "$PART" ]; then
    PARENT_RESOURCE_ID=$(get_or_create_resource_id $PARENT_RESOURCE_ID $PART)
  fi
done

# Vincular el método a Lambda en el último recurso
aws apigateway put-method --rest-api-id ${API_ID} --resource-id ${PARENT_RESOURCE_ID} --http-method ${METHOD} --authorization-type "NONE" --region ${REGION} --no-paginate

aws apigateway put-integration --rest-api-id ${API_ID} --resource-id ${PARENT_RESOURCE_ID} --http-method ${METHOD} --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${LAMBDA_FUNCTION_NAME}/invocations --region ${REGION} --no-paginate


# Implementar los cambios en la etapa correspondiente (stage)
aws apigateway create-deployment --rest-api-id ${API_ID} --stage-name ${STAGE} --region ${REGION}
echo "Despliegue realizado en el stage ${STAGE}."


