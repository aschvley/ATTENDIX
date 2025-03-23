from database.db import get_connection

def mostrar_asistencias():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.nombre, e.cedula, a.fecha
        FROM asistencias a
        JOIN estudiantes e ON a.estudiante_id = e.id
        ORDER BY a.fecha DESC
    """)

    resultados = cursor.fetchall()
    print("\n📝 REGISTRO DE ASISTENCIAS\n----------------------------")
    for nombre, cedula, fecha in resultados:
        print(f"{fecha} - {nombre} ({cedula})")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    mostrar_asistencias()
