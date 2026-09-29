import sqlite3

DB_NAME = "hospital.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT DEFAULT 'Booked',
            UNIQUE(doctor_id, appointment_date, appointment_time)
        )
    """)

    doctors = [
        ("Dr. Arun Kumar", "Cardiology"),
        ("Dr. Priya Sharma", "Dermatology"),
        ("Dr. Ravi Kumar", "General Medicine"),
        ("Dr. Meena Devi", "Pediatrics")
    ]

    count = connection.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    if count == 0:
        connection.executemany(
            "INSERT INTO doctors (name, specialization) VALUES (?, ?)",
            doctors
        )

    connection.commit()
    connection.close()


def get_doctors():
    connection = get_connection()

    doctors = connection.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    connection.close()

    return doctors


def book_appointment(patient_name, doctor_id, date, time):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO appointments
            (patient_name, doctor_id, appointment_date, appointment_time)
            VALUES (?, ?, ?, ?)
        """, (patient_name, doctor_id, date, time))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_appointments():
    connection = get_connection()

    appointments = connection.execute("""
        SELECT
            appointments.*,
            doctors.name AS doctor_name,
            doctors.specialization
        FROM appointments
        JOIN doctors
        ON appointments.doctor_id = doctors.id
        ORDER BY appointment_date, appointment_time
    """).fetchall()

    connection.close()

    return appointments