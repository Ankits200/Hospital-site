from io import BytesIO
from flask import render_template, redirect, request, send_file, url_for, flash, jsonify
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, UserMixin, logout_user
from sqlalchemy.exc import IntegrityError
from app.forms import MyForm, addForm,searchForm
from .models import Patients,db

from . import app, login_manager

class Admin(UserMixin):
    id = 1
    username = app.config['ADMIN_USERNAME']

@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        return Admin()
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        if name and email and subject and message:
            return jsonify({'message': 'Message sent successfully!'}), 200
        else:
            return jsonify({'message': 'Failed to send message.'}), 400
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = MyForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == app.config['ADMIN_USERNAME'] and check_password_hash(generate_password_hash(app.config['ADMIN_PASSWORD'], method="scrypt", salt_length=16), password):
            login_user(Admin())
            flash("logged in successfully",'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    patients = db.session.query(Patients).all()
    return render_template("dashboard.html",patients=patients)

@app.route("/add",methods = ["GET","POST"])
@login_required
def add():
    form = addForm()
    if request.method == "POST" and form.validate_on_submit():
        
        name = form.name.data
        address = form.address.data 
        contact = form.contact.data
        age = form.age.data
        date = form.date.data
        UHID = form.UHID.data
        opd =  form.opd.data
        consultantName = form.consultantName.data
        newPatient = Patients(
            Name = name,
            Address = address,
            Contact = contact,
            Age = age,
            date =date,
            UHID = UHID,
            opd = opd,
            consultantName = consultantName
        )
        try:
            db.session.add(newPatient)
            db.session.commit()
            flash("Patient successfully added in the database",'success')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            flash("Patient with this UHID already exists",'danger')
        

    return render_template("add.html",form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/delete",methods=["GET","POST"])
@login_required
def delete():
    idv = request.args.get('id')
    patient = db.get_or_404(Patients,idv)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/search",methods=["GET","POST"])
@login_required
def search():
    form = searchForm()
    patients =[]
    if request.method == "POST" and form.validate_on_submit():
        UHID = form.UHID.data
        patients = Patients.query.filter_by(UHID=UHID).all()
        if not patients:
            flash("No patient found with this UHID", 'danger')
    
    return render_template("search.html", form=form,patients=patients)

@app.route('/export_excel')
@login_required
def export_excel():
    # Query all patients from the database
    patients = Patients.query.all()
    
    # Convert the query result to a list of dictionaries
    data = [
        {
            "Sr no.": index + 1,
            "Name": patient.Name,
            "Address": patient.Address,
            "Contact": patient.Contact,
            "Age": patient.Age,
            "Date": patient.date,
            "UHID": patient.UHID,
            "OPD": patient.opd,
            "Consultant Name": patient.consultantName,
        }
        for index, patient in enumerate(patients)
    ]
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    
    # Create a BytesIO buffer to hold the Excel file in memory
    buffer = BytesIO()
    
    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Patients')
    
    # Rewind the buffer
    buffer.seek(0)
    
    # Send the file as an attachment
    return send_file(buffer, as_attachment=True, download_name='patients.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
@app.route('/print_patients')
@login_required
def print_patients():
    # Query all patients from the database
    patients = Patients.query.all()
    return render_template('print_patients.html', patients=patients)
