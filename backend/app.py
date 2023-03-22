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


if __name__ == '__main__':
    app.run()
