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

    prev_government_domains_stats = state.prev_government_domains_stats
    prev_social_domains_stats = state.prev_social_domains_stats
    prev_top_domains_stats = state.prev_top_domains_stats

    context = {
        'site_list': 'site_list',
        'actual_entries_count': state.actual_entries_count,
        'gov_ca_count': 0 if len(state.actual_government_domains_stats[0][0]) == 0 else len(
            state.actual_government_domains_stats[0][0].split(',')),
        'gov_ss_count': 0 if len(state.actual_government_domains_stats[1][0]) == 0 else len(
            state.actual_government_domains_stats[1][0].split(',')),
        'social_ca_count': 0 if len(state.actual_social_domains_stats[0][0]) == 0 else len(
            state.actual_social_domains_stats[0][0].split(',')),
        'social_ss_count': 0 if len(state.actual_social_domains_stats[1][0]) == 0 else len(
            state.actual_social_domains_stats[1][0].split(',')),
        'top_ca_count': 0 if len(state.actual_top_domains_stats[0][0]) == 0 else len(
            state.actual_top_domains_stats[0][0].split(',')),
        'top_ss_count': 0 if len(state.actual_top_domains_stats[1][0]) == 0 else len(
            state.actual_top_domains_stats[1][0].split(',')),
        'int': int,  # pass the int() function to the context
        'round': round  # pass the abs() function to the context
    }

    return render_template('index.html', **context)


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
