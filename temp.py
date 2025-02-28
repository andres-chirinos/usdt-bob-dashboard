from faker import Faker

import mysql.connector

# Configuración de la conexión a la base de datos
config = {"user": "root", "password": "", "host": "localhost", "database": "test"}

# Crear una instancia de Faker
fake = Faker()

# Conectar a la base de datos
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def estudiantes():
    # Generar datos de prueba y insertarlos en la tabla estudiantes
    for _ in range(15):  # Generar 100 registros de prueba
        nombre = fake.first_name()
        apellido = fake.last_name()
        fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=25)
        correo_electronico = fake.unique.email()
        telefono = fake.phone_number()
        direccion = fake.address()
        genero = fake.random_element(elements=("M", "F", "O"))

        query = """
        INSERT INTO estudiantes (nombre, apellido, fecha_nacimiento, correo_electronico, telefono, direccion, genero)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            nombre,
            apellido,
            fecha_nacimiento,
            correo_electronico,
            telefono,
            direccion,
            genero,
        )

        cursor.execute(query, values)

def materias():
    # Generar datos de prueba y insertarlos en la tabla materias
    for _ in range(10):  # Generar 15 registros de prueba
        nombre_materia = fake.word().capitalize()
        codigo_materia = fake.unique.bothify(text="???-###")
        descripcion_materia = fake.text(max_nb_chars=200)
        creditos_materia = fake.random_int(min=1, max=10)
        activo_materia = fake.boolean()

        query_materias = """
        INSERT INTO materias (nombre, codigo, descripcion, creditos, activo)
        VALUES (%s, %s, %s, %s, %s)
        """
        values_materias = (
            nombre_materia,
            codigo_materia,
            descripcion_materia,
            creditos_materia,
            activo_materia,
        )

        cursor.execute(query_materias, values_materias)

def relaciones():
    # Obtener los IDs de estudiantes y materias
    cursor.execute("SELECT id FROM estudiantes")
    estudiantes_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM materias")
    materias_ids = [row[0] for row in cursor.fetchall()]

    # Generar datos de prueba y insertarlos en la tabla clases
    for _ in range(75):  # Generar 75 registros de prueba
        estudiante_id = fake.random_element(estudiantes_ids)
        materia_id = fake.random_element(materias_ids)
        fecha_inscripcion = fake.date_time_this_year()
        estado = fake.random_element(elements=("Inscrito", "Aprobado", "Reprobado"))

        # Verificar si la combinación de estudiante_id y materia_id ya existe en la base de datos
        cursor.execute(
            "SELECT COUNT(*) FROM clases WHERE estudiante_id = %s AND materia_id = %s",
            (estudiante_id, materia_id),
        )
        if cursor.fetchone()[0] > 0:
            continue

        query_clases = """
        INSERT INTO clases (estudiante_id, materia_id, fecha_inscripcion, estado)
        VALUES (%s, %s, %s, %s)
        """
        values_clases = (
            estudiante_id,
            materia_id,
            fecha_inscripcion,
            estado,
        )

        cursor.execute(query_clases, values_clases)

#estudiantes()
#materias()
#relaciones()
# Confirmar los cambios
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
