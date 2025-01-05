from sqlalchemy import text
from database import engine


def test_connection():
    """Intenta realizar una consulta simple para probar la conexión a la base de datos."""
    try:
        print(engine)
        with engine.connect() as connection:
            print("PRUEBA")
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
