import os
import sys
import json
from dotenv import load_dotenv
import requests
import boto3

load_dotenv()

class APIGatewayDeployer:
    def __init__(self):
        self.apigateway = boto3.client('apigateway')
        self.region = os.environ['AWS_REGION']
        self.api_name = os.environ['AWS_API_NAME']
        self.lambda_function_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']
        self.account_id = os.environ['AWS_ACCOUNT_ID']

    def get_api_id(self):
        """Obtener ID de API Gateway"""
        apis =self.apigateway.get_rest_apis()
        for api in apis['items']:
            if api['name'] == self.api_name:
                return api['id']
        raise ValueError(f"No se encontró API con nombre {self.api_name}")

    def get_route_info(self, code_id: str):
        """Obtener información de ruta desde OpenAPI"""
        url = "http://127.0.0.1:8000/openapi.json"
        response = requests.get(url)
        openapi_schema = response.json()

        for path, methods in openapi_schema['paths'].items():
            for method, info in methods.items():
                if info.get('operationId') == code_id:
                    return {
                        'path': path,
                        'method': method.upper(),
                        'code_id': code_id
                    }
        raise ValueError(f"No se encontró ruta para code_id: {code_id}")

    def create_or_get_resource(self, api_id, parent_id, path_part):
        """Crear o recuperar recurso en API Gateway"""
        resources = self.apigateway.get_resources(restApiId=api_id)
        for resource in resources['items']:
            if resource.get('pathPart') == path_part and resource.get('parentId') == parent_id:
                return resource['id']

        new_resource = self.apigateway.create_resource(
            restApiId=api_id,
            parentId=parent_id,
            pathPart=path_part
        )
        return new_resource['id']

    def deploy_api(self, code_id, stage):
        try:
            api_id = self.get_api_id()
            route_info = self.get_route_info(code_id)

            # Obtener recurso raíz
            root_resources = self.apigateway.get_resources(restApiId=api_id)
            root_resource_id = next(
                r['id'] for r in root_resources['items']
                if r['path'] == '/'
            )

            # Crear recursos recursivamente
            current_resource_id = root_resource_id
            path_parts = route_info['path'].strip('/').split('/')

            for part in path_parts:
                current_resource_id = self.create_or_get_resource(
                    api_id, current_resource_id, part
                )

            # Verificar si el método ya existe
            try:
                # Intentar obtener el método existente
                self.apigateway.get_method(
                    restApiId=api_id,
                    resourceId=current_resource_id,
                    httpMethod=route_info['method']
                )
                print(f"Método {route_info['method']} ya existe. Actualizando...")
            except self.apigateway.exceptions.NotFoundException:
                # Si no existe, crear método
                self.apigateway.put_method(
                    restApiId=api_id,
                    resourceId=current_resource_id,
                    httpMethod=route_info['method'],
                    authorizationType='NONE'
                )

            # Configurar integración Lambda (siempre actualizar)
            self.apigateway.put_integration(
                restApiId=api_id,
                resourceId=current_resource_id,
                httpMethod=route_info['method'],
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{self.region}:{self.account_id}:function:{self.lambda_function_name}/invocations'
            )

            # Crear despliegue
            self.apigateway.create_deployment(
                restApiId=api_id,
                stageName=stage
            )

            print(f"Despliegue realizado en stage {stage}")

        except Exception as e:
            print(f"Error en despliegue: {e}")
            sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Uso: python deploy_api.py <code_id> <stage>")
        sys.exit(1)

    deployer = APIGatewayDeployer()
    deployer.deploy_api(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()