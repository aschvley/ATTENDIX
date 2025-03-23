# attendance/attendance.py
from database.db import get_connection

def registrar_asistencia(estudiante_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO asistencias (estudiante_id) VALUES (%s)"
    cursor.execute(sql, (estudiante_id,))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Asistencia registrada para ID {estudiante_id}.")
