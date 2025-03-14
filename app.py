from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "rahasia_admin"  # Kunci rahasia untuk sesi login

EXCEL_FILE = "zakat_data.xlsx"

# Data login admin (ganti sesuai kebutuhan)
ADMIN_USERNAME = "dpcbtg"
ADMIN_PASSWORD = "dpcbtg"

# Fungsi untuk memuat data dari Excel
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=["Nama", "Zakat Fitrah", "Zakat Kifarat", "Zakat Harta"])

# Fungsi untuk menyimpan data ke Excel
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

# Halaman utama (user hanya bisa melihat data)
@app.route('/')
def index():
    df = load_data()
    return render_template('index.html', data=df.to_dict(orient='records'), is_admin=session.get('is_admin', False))

# Halaman login admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True  # Set session admin
            return redirect(url_for('index'))
        else:
            return "Login gagal. Coba lagi!"
    return render_template('login.html')

# Logout admin
@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

# Route untuk download Excel (hanya untuk admin)
@app.route('/download-excel')
def download_excel():
    if session.get('is_admin'):
        return send_file(EXCEL_FILE, as_attachment=True)
    else:
        return "Akses ditolak. Anda bukan admin!"

if __name__ == '__main__':
    app.run(debug=True)
