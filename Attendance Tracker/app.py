import csv
import io
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, Response

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = "super_secret_key"  # Needed for flash messages

TRAINEES_FILE = os.path.join(os.path.dirname(__file__), "trainees.csv")
ATTENDANCE_FILE = os.path.join(os.path.dirname(__file__), "attendance.csv")


def init_csv_files():
    if not os.path.exists(TRAINEES_FILE):
        with open(TRAINEES_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name'])
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['trainee_id', 'date', 'status'])


def read_trainees():
    trainees = []
    if os.path.exists(TRAINEES_FILE):
        with open(TRAINEES_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trainees.append(row)
    return trainees


def read_attendance():
    attendance = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                attendance.append(row)
    return attendance


def save_trainee(trainee_id, trainee_name):
    with open(TRAINEES_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([trainee_id, trainee_name])


def save_attendance(records):
    existing = read_attendance()
    record_map = {(r['trainee_id'], r['date']): r['status'] for r in existing}
    
    for r in records:
        record_map[(r['trainee_id'], r['date'])] = r['status']
        
    with open(ATTENDANCE_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['trainee_id', 'date', 'status'])
        for (tid, d), status in record_map.items():
            writer.writerow([tid, d, status])


@app.route("/")
def index():
    selected_date = request.args.get("date", date.today().isoformat())
    trainees = read_trainees()
    attendance = read_attendance()
    
    attendance_map = {(r['trainee_id'], r['date']): r['status'] for r in attendance}
    
    trainees_for_date = []
    for t in trainees:
        status = attendance_map.get((t['id'], selected_date), 'Present')
        trainees_for_date.append({
            'id': t['id'],
            'name': t['name'],
            'status': status
        })
        
    report_data = []
    for t in trainees:
        t_id = t['id']
        t_name = t['name']
        t_records = [r for r in attendance if r['trainee_id'] == t_id]
        total_days = len(t_records)
        present = sum(1 for r in t_records if r['status'] == 'Present')
        absent = sum(1 for r in t_records if r['status'] == 'Absent')
        percentage = round((present / total_days) * 100, 1) if total_days > 0 else 0.0
        report_data.append({
            'id': t_id,
            'name': t_name,
            'total_days': total_days,
            'present': present,
            'absent': absent,
            'percentage': f"{percentage:g}"
        })
        
    return render_template(
        "index.html",
        trainees=trainees_for_date,
        report=report_data,
        selected_date=selected_date
    )


@app.route("/register", methods=["POST"])
def register_trainee():
    trainee_id = request.form.get("trainee_id", "").strip()
    trainee_name = request.form.get("trainee_name", "").strip()
    
    if not trainee_id or not trainee_name:
        flash("Trainee ID and Name are required.", "error")
        return redirect(url_for("index"))
        
    trainees = read_trainees()
    if any(t['id'] == trainee_id for t in trainees):
        flash(f"Trainee ID '{trainee_id}' already exists.", "error")
        return redirect(url_for("index"))
        
    save_trainee(trainee_id, trainee_name)
    flash("Trainee registered successfully.", "success")
    return redirect(url_for("index"))


@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    target_date = request.form.get("attendance_date", "").strip()
    if not target_date:
        flash("Date is required.", "error")
        return redirect(url_for("index"))
        
    records = []
    for key, value in request.form.items():
        if key.startswith("status_"):
            trainee_id = key.replace("status_", "")
            if value not in ("Present", "Absent"):
                value = "Present"
            records.append({
                "trainee_id": trainee_id,
                "date": target_date,
                "status": value
            })
            
    save_attendance(records)
    flash(f"Attendance saved for {target_date}.", "success")
    return redirect(url_for("index", date=target_date))


@app.route("/export")
def export_report():
    trainees = read_trainees()
    attendance = read_attendance()
    report_data = []
    for t in trainees:
        t_id = t['id']
        t_name = t['name']
        t_records = [r for r in attendance if r['trainee_id'] == t_id]
        total_days = len(t_records)
        present = sum(1 for r in t_records if r['status'] == 'Present')
        absent = sum(1 for r in t_records if r['status'] == 'Absent')
        percentage = round((present / total_days) * 100, 1) if total_days > 0 else 0.0
        report_data.append({
            'id': t_id,
            'name': t_name,
            'total_days': total_days,
            'present': present,
            'absent': absent,
            'percentage': f"{percentage:g}"
        })
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Trainee ID", "Trainee Name", "Total Days", "Present", "Absent", "Attendance %"])
    for row in report_data:
        writer.writerow([
            row["id"],
            row["name"],
            row["total_days"],
            row["present"],
            row["absent"],
            f"{row['percentage']}%"
        ])
    csv_content = output.getvalue()
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_report.csv"}
    )


if __name__ == "__main__":
    init_csv_files()
    app.run(debug=True, port=5000)
