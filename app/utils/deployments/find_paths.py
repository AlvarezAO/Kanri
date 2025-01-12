import requests
import json
import sys

# URL del schema OpenAPI generado por FastAPI
url = "http://127.0.0.1:8000/openapi.json"


# Función para obtener las rutas desde el OpenAPI schema
def obtener_rutas(code_id_buscado):
    response = requests.get(url)
    openapi_schema = json.loads(response.text)

    # Buscar la ruta que coincida con el code_id
    for path, methods in openapi_schema['paths'].items():
        for method, info in methods.items():
            code_id = info.get('operationId', None)
            if code_id == code_id_buscado:
                return {
                    'path': path,
                    'method': method.upper(),
                    'code_id': code_id
                }
    return None


# Obtener el code_id pasado como argumento en el script bash
code_id_buscado = sys.argv[1]

# Obtener la ruta correspondiente al code_id
ruta = obtener_rutas(code_id_buscado)

# Si encontramos la ruta, imprimimos el JSON
if ruta:
    print(json.dumps(ruta))
else:
    print(json.dumps({'error': 'No se encontro la ruta para el code_id proporcionado.'}))
