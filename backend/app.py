import os
from datetime import date

from flask import Flask, render_template, send_file

from utils import common, db
from utils.StatsState import StatsState

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')

state = StatsState()
state.init_cache()


@app.route('/')
def index():
    state.update_cache(date.today())

    total_count_in_categories = state.actual_entries_count

    total_actual_gov_stats = state.actual_government_domains_stats
    total_actual_social_stats = state.actual_social_domains_stats
    total_actual_top_stats = state.actual_top_domains_stats

    total_prev_gov_stats = state.prev_government_domains_stats
    total_prev_social_stats = state.prev_social_domains_stats
    total_prev_top_stats = state.prev_top_domains_stats

    return render_template('index.html',
                           site_list="site_list",
                           total_count=total_count_in_categories
                           )


@app.route('/download_dump')
def download_dump():
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'analyser',
        'statistics.db')
    return send_file(file_path, as_attachment=True, mimetype='application/x-sqlite3')


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
