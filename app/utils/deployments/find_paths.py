import requests
import json

# URL del schema OpenAPI generado por FastAPI
url = "http://127.0.0.1:8000/openapi.json"


def obtener_rutas():
    response = requests.get(url)
    openapi_schema = json.loads(response.text)

    rutas = []

    for path, methods in openapi_schema['paths'].items():
        for method, info in methods.items():
            code_id = info.get('operationId', None)
            if code_id:
                rutas.append({
                    'path': path,
                    'method': method.upper(),
                    'code_id': code_id
                })
    return rutas


rutas = obtener_rutas()
for ruta in rutas:
    print(f"Ruta: {ruta['path']}, Método: {ruta['method']}, Code ID: {ruta['code_id']}")
