from ftplib import FTP
from flask import Flask, request, render_template

app = Flask(__name__)

# Konfigurasi FTP
ftp_host = 'ftp.dlptest.com'
ftp_user = 'dlpuser'
ftp_password = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

# Fungsi untuk mengupload file ke server FTP
def upload_file(file_path):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)

    with open(file_path, 'rb') as file:
        ftp.storbinary('STOR {}'.format(file_path), file)

    ftp.quit()

# Fungsi untuk mengunduh file dari server FTP
def download_file(file_name):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)

    with open(file_name, 'wb') as file:
        ftp.retrbinary('RETR {}'.format(file_name), file.write)

    ftp.quit()

# Route utama
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'upload_file' in request.files:
            file = request.files['upload_file']
            file.save(file.filename)
            upload_file(file.filename)
            return 'File {} berhasil diunggah ke server FTP.'.format(file.filename)
        elif 'download_file' in request.form:
            file_name = request.form['download_file']
            download_file(file_name)
            return 'File {} berhasil diunduh dari server FTP.'.format(file_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
