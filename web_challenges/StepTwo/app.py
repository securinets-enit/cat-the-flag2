from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file, render_template_string
from weasyprint import HTML
from io import BytesIO
import os
import database
from datetime import datetime
from jinja2 import *  # Import Template for SSTI vulnerability

app = Flask(__name__)
app.secret_key = 'SecretSupercode11254'  # Change this in production!

# Set the flag as an environment variable
os.environ['FLAG'] = "SecurinetsENIT{c96ebab349abb03c26b0824b9d2bf2cb769294f5ea271ace67a085d019ccabf4}"

# Initialize database
database.init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']

        if database.get_user_by_username(username):
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if database.create_user(username, password, full_name):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = database.get_user_by_username(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    certificates = database.get_user_certificates(session['user_id'])
    user = database.get_user_by_id(session['user_id'])        # fetch current user
    return render_template(
        'dashboard.html',
        certificates=certificates,
        user=user                                           # pass it to template
    )



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    user = database.get_user_by_id(session['user_id'])

    if request.method == 'POST':
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        phone = request.form['phone']

        database.update_profile(session['user_id'], date_of_birth, address, phone)
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)


@app.route('/certificate')
def certificate():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    certificates = database.get_user_certificates(session['user_id'])
    return render_template('certificate.html', certificates=certificates)


@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    course_name = request.form['course_name']
    user = database.get_user_by_id(session['user_id'])
    issue_date = datetime.now().strftime("%Y-%m-%d")

    # Dark-themed professional certificate template
    template_string = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Certificate of Completion</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

            /* Set page size for A4 landscape */
            @page {{
                size: A4 landscape;
                margin: 0;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: 'Montserrat', sans-serif;
                background: #1a1a1a;
                color: #f5f5f5;
                width: 297mm; /* A4 landscape width */
                height: 210mm; /* A4 landscape height */
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .certificate-container {{
                width: 280mm; /* Slightly less than full page width for margins */
                height: 180mm; /* Slightly less than full page height for margins */
                padding: 15mm;
                border: 8px solid #444;
                background: linear-gradient(135deg, #2c2c2c, #1a1a1a);
                box-shadow: 0 0 30px rgba(0,0,0,0.7);
                text-align: center;
                position: relative;
                box-sizing: border-box;
            }}

            .certificate-title {{
                font-size: 20px;
                font-weight: 700;
                color: #e0a800;
                margin-bottom: 10px;
                letter-spacing: 2px;
            }}

            .certificate-subtitle {{
                font-size: 18px;
                color: #ccc;
                margin-bottom: 20px;
            }}

            .certificate-name {{
                font-size: 20px;
                font-weight: 700;
                color: #fff;
                margin: 25px 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            }}

            .certificate-course {{
                font-size: 22px;
                color: #f5f5f5;
                margin: 25px 0;
                font-style: italic;
                line-height: 1.4;
            }}

            .certificate-date {{
                font-size: 16px;
                margin-top: 25px;
                color: #aaa;
            }}

            .signature {{
                margin-top: 40px;
                display: flex;
                justify-content: space-around;
                align-items: center;
                padding: 0 40px;
            }}

            .signature-block {{
                text-align: center;
                flex: 1;
            }}

            .signature-block img {{
                width: 150px;
                height: auto;
            }}

            .signature-text {{
                margin-top: 5px;
                font-size: 14px;
                color: #f5f5f5;
                font-weight: 700;
            }}

            .ribbon {{
                width: 150px;
                height: 30px;
                background: #e0a800;
                color: #1a1a1a;
                font-weight: bold;
                position: absolute;
                top: 20px;
                right: -40px;
                transform: rotate(45deg);
                text-align: center;
                line-height: 30px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}

            /* Print styles */
            @media print {{
                body {{
                    width: 297mm;
                    height: 210mm;
                    background: #1a1a1a;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }}

                .certificate-container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="certificate-container">
            <div class="ribbon">CERTIFIED</div>
            <h1 class="certificate-title">Certificate of Completion</h1>
            <p class="certificate-subtitle">This is to certify that</p>
            <h2 class="certificate-name">{user['full_name']}</h2>
            <p class="certificate-course">has successfully completed the course<br>"{course_name}"</p>
            <p class="certificate-date">Issued on: <strong>{issue_date}</strong></p>

            <div class="signature">
                <div class="signature-block">
                    <img src="/static/signature.png" alt="Signature">
                    <p class="signature-text">School Principal</p>
                </div>
                <div class="signature-block">
                    <img src="/static/seal.png" alt="Seal">
                    <p class="signature-text">Official Seal</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Render template with SSTI vulnerability
    certificate_content = render_template_string(template_string)
    database.add_certificate(session['user_id'], course_name, issue_date, certificate_content)

    flash('Professional dark-themed certificate generated successfully!', 'success')
    return redirect(url_for('certificate'))


@app.route('/download_certificate/<int:cert_id>')
def download_certificate(cert_id):
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    conn = database.get_db_connection()
    certificate = conn.execute(
        'SELECT * FROM certificates WHERE id = ? AND user_id = ?',
        (cert_id, session['user_id'])
    ).fetchone()
    conn.close()

    if not certificate:
        flash('Certificate not found', 'danger')
        return redirect(url_for('certificate'))

    # Use WeasyPrint to render the HTML certificate to PDF
    pdf_file = BytesIO()
    HTML(string=certificate['certificate_data'], base_url=request.host_url).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=f"certificate_{certificate['course_name']}.pdf",
        mimetype='application/pdf'
    )


@app.route('/timetable')
def timetable():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    return render_template('timetable.html')


@app.route('/absences', methods=['GET', 'POST'])
def absences():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    absences = database.get_absences()
    return render_template('absences.html', absences=absences)


@app.route('/report_absence', methods=['POST'])
def report_absence():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    date = request.form['date']
    reason = request.form['reason']
    student_id = session['user_id']

    database.add_absence(student_id, date, reason)
    flash('Absence reported successfully', 'success')
    return redirect(url_for('absences'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
