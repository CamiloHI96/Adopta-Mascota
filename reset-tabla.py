import sqlite3

def truncate_tables():
    try:
        conn = sqlite3.connect('instance/adopta_mascotas.db')
        cursor = conn.cursor()

        # Lista de tablas a truncar
        tables = ['users', 'refugios', 'mascotas']

        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
            print(f"Datos de la tabla '{table}' eliminados.")

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error al truncar las tablas: {e}")

# Llamada a la función para truncar las tablas
truncate_tables()
