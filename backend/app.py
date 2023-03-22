import os

from flask import Flask, Response, render_template, send_file

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download_dump')
def download_dump():
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'analyser',
        'statistics.db')
    return send_file(file_path, as_attachment=True, mimetype='application/x-sqlite3')


@app.route('/download_ca_list')
def download_ca_list():
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'analyser',
        'ssl_cert_err.txt')
    return send_file(file_path, as_attachment=True, mimetype='text/plain')


@app.route('/download_self_sign_list')
def download_self_sign_list():
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'analyser',
        'ssl_self_sign_err.txt')
    return send_file(file_path, as_attachment=True, mimetype='text/plain')


if __name__ == '__main__':
    app.run()
