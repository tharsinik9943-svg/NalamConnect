from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, book_appointment, get_appointments
from cache import get_cached_doctors

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/doctors")
def doctors():
    doctors = get_cached_doctors()
    return render_template("doctors.html", doctors=doctors)


@app.route("/book", methods=["GET", "POST"])
def book():
    doctors = get_cached_doctors()

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        doctor_id = request.form["doctor_id"]
        date = request.form["date"]
        time = request.form["time"]

        success = book_appointment(
            patient_name,
            doctor_id,
            date,
            time
        )

        if success:
            return redirect(url_for("appointments"))

        return "This appointment slot is already booked!"

    return render_template("book.html", doctors=doctors)


@app.route("/appointments")
def appointments():
    appointments = get_appointments()
    return render_template(
        "appointments.html",
        appointments=appointments
    )
@app.route("/api/doctors")
def api_doctors():

    doctors = get_cached_doctors()

    doctor_list = []

    for doctor in doctors:
        doctor_list.append({
            "id": doctor["id"],
            "name": doctor["name"],
            "specialization": doctor["specialization"]
        })

    return jsonify(doctor_list)
@app.route("/api/appointments")
@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():

    # GET - View appointments
    if request.method == "GET":

        appointments = get_appointments()

        appointment_list = []

        for appointment in appointments:
            appointment_list.append({
                "id": appointment["id"],
                "patient_name": appointment["patient_name"],
                "doctor_name": appointment["doctor_name"],
                "specialization": appointment["specialization"],
                "date": appointment["appointment_date"],
                "time": appointment["appointment_time"],
                "status": appointment["status"]
            })

        return jsonify(appointment_list)

    # POST - Create appointment
    data = request.get_json()

    patient_name = data["patient_name"]
    doctor_id = data["doctor_id"]
    date = data["date"]
    time = data["time"]

    success = book_appointment(
        patient_name,
        doctor_id,
        date,
        time
    )

    if success:
        return jsonify({
            "message": "Appointment booked successfully!"
        }), 201

    return jsonify({
        "message": "This appointment slot is already booked!"
    }), 409

if __name__ == "__main__":
    app.run(debug=True)