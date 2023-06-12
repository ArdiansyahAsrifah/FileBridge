from ftplib import FTP
from flask import Flask, request, render_template, redirect
from io import BytesIO

app = Flask(__name__)

# Konfigurasi FTP
ftp_host = 'ftp.dlptest.com'
ftp_user = 'dlpuser'
ftp_password = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

# Fungsi untuk mengupload file ke server FTP
def upload_file(file):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)

    # Membaca file dari objek BytesIO
    file_data = file.stream.read()

    # Mengirim file sebagai BytesIO ke server FTP
    ftp.storbinary('STOR {}'.format(file.filename), BytesIO(file_data))

    ftp.quit()

# Fungsi untuk mengunduh file dari server FTP
def download_file(file_name):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)

    # Membuka file sebagai BytesIO
    file_data = BytesIO()

    # Mengunduh file dari server FTP ke BytesIO
    ftp.retrbinary('RETR {}'.format(file_name), file_data.write)

    # Mengembalikan data file yang diunduh
    file_data.seek(0)
    return file_data

# Fungsi untuk mendapatkan daftar file di server FTP
def get_file_list():
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)

    file_list = ftp.nlst()

    ftp.quit()

    return file_list

# Route utama
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'upload_file' in request.files:
            file = request.files['upload_file']
            if file.filename == '':
                return render_template('index.html', error_message='Mohon pilih file yang ingin diunggah')
            upload_file(file)
            return render_template('uploaded.html')
        elif 'download_file' in request.form:
            file_name = request.form['download_file']
            if file_name == '':
                return render_template('index.html', error_message='Mohon masukkan nama file yang ingin diunduh')
            file_data = download_file(file_name)
            return redirect('/download/{}'.format(file_name))

    file_list = get_file_list()
    return render_template('index.html', file_list=file_list)

# Route unduhan file
@app.route('/download/<path:file_name>')
def download(file_name):
    file_data = download_file(file_name)
    return app.response_class(file_data, mimetype='application/octet-stream', direct_passthrough=True)

# Route setelah mengunggah file
@app.route('/uploaded')
def uploaded():
    return render_template('uploaded.html')

# Route ingin melihat file list
@app.route('/ftp')
def ftp_file_list():
    file_list = get_file_list()
    return render_template('ftp_file_list.html', file_list=file_list)


if __name__ == '__main__':
    app.run(debug=True)
