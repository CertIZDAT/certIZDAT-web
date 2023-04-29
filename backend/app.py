import os
import sqlite3

from flask import Flask, render_template, send_file

from analyser.check import db_name as db_name
from utils import common, db

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')


@app.route('/')
def index():
    try:
        connection = db.get_db_connection(f'../analyser/{db_name}')
    except sqlite3.Error as e:
        print(f'get db connection error: {e}')

    err_info = ''
    try:
        dataset_size = common.get_total_dataset_size(connection)
        site_list = common.get_latest_list_results(connection, 'CA')

        ca_count_last_month = common.get_latest_counts(connection, 'CA')
        ca_stats = (ca_count_last_month,
                    ca_count_last_month * 100 / dataset_size)

        ss_count_last_month = common.get_latest_counts(connection, 'SS')
        ss_stats = (ss_count_last_month,
                    ss_count_last_month * 100 / dataset_size)

        # setup analysis later
        diff = ('773 / 3.44%', '176 / 0.78%')
    except sqlite3.Error as e:
        print(f'db connection error: {e}')
        err_info = f'db connection error: {e}'
    finally:
        connection.close()

    if err_info:
        return render_template('err.html', err_info=err_info)

    return render_template('index.html',
                           site_list=site_list,
                           dataset_size=dataset_size,
                           ca_stats=ca_stats,
                           ss_stats=ss_stats,
                           diff=diff)


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
    res = common.get_latest_list_results(connection, 'CA')
    connection.close()
    return res


@app.route('/process/self-sign')
def self_sign():
    connection = db.get_db_connection('../analyser/statistics.db')
    res_list = common.get_latest_list_results(connection, 'SS')
    connection.close()
    return res_list


# 404 page


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
