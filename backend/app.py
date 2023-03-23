import os

from flask import Flask, render_template, send_file

from utils import common, db

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')


@app.route('/')
def index():
    # TODO: Read db_name from what??
    connection = db.get_db_connection('../analyser/statistics.db')

    site_list = common.get_latest_list_results(connection, 'CA')
    update_time = common.get_last_update_time(connection)

    stats = (common.get_latest_counts(
        connection, 'CA'), common.get_total_dataset_size(connection))

    connection.close()
    return render_template('index.html', site_list=site_list,
                           update_time=update_time,
                           stats=stats)


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


@app.route('/process/russian-trusted-ca')
def russian_trusted_ca():
    connection = db.get_db_connection('../analyser/statistics.db')
    list = common.get_latest_list_results(connection, 'CA')
    connection.close()
    return list


@app.route('/process/self-sign')
def self_sign():
    connection = db.get_db_connection('../analyser/statistics.db')
    list = common.get_latest_list_results(connection, 'SS')
    connection.close()
    return list

# 404 page


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
