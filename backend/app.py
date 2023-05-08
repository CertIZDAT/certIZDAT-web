import os
from datetime import date

from flask import Flask, render_template, send_file

from utils import common, db
from utils.StatsState import StatsState
from utils.common import get_diff_and_color

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')

state = StatsState()
state.init_cache()


@app.route('/')
def index():
    state.update_cache(date.today())

    gov_ca_count = len(state.actual_government_domains_stats[0][0].split(',')) if \
        state.actual_government_domains_stats[0][0] else 0
    gov_ss_count = len(state.actual_government_domains_stats[1][0].split(',')) if \
        state.actual_government_domains_stats[1][0] else 0
    social_ca_count = len(state.actual_social_domains_stats[0][0].split(',')) if state.actual_social_domains_stats[0][
        0] else 0
    social_ss_count = len(state.actual_social_domains_stats[1][0].split(',')) if state.actual_social_domains_stats[1][
        0] else 0
    top_ca_count = len(state.actual_top_domains_stats[0][0].split(',')) if state.actual_top_domains_stats[0][0] else 0
    top_ss_count = len(state.actual_top_domains_stats[1][0].split(',')) if state.actual_top_domains_stats[1][0] else 0

    context = {
        'site_list': 'site_list',
        'actual_entries_count': state.actual_entries_count,
        'gov_ca_count': gov_ca_count,
        'gov_ss_count': gov_ss_count,
        'social_ca_count': social_ca_count,
        'social_ss_count': social_ss_count,
        'top_ca_count': top_ca_count,
        'top_ss_count': top_ss_count
    }

    # Get the government diffs
    gov_ca_diff, gov_ca_color = get_diff_and_color(
        state.actual_government_domains_stats[0][0], state.prev_government_domains_stats[0][0])
    gov_ss_diff, gov_ss_color = get_diff_and_color(
        state.actual_government_domains_stats[1][0], state.prev_government_domains_stats[1][0])

    # Get the social diffs
    social_ca_diff, social_ca_color = get_diff_and_color(
        state.actual_social_domains_stats[0][0], state.prev_social_domains_stats[0][0])
    social_ss_diff, social_ss_color = get_diff_and_color(
        state.actual_social_domains_stats[1][0], state.prev_social_domains_stats[1][0])

    # Get the top diffs
    top_ca_diff, top_ca_color = get_diff_and_color(
        state.actual_top_domains_stats[0][0], state.prev_top_domains_stats[0][0])
    top_ss_diff, top_ss_color = get_diff_and_color(
        state.actual_top_domains_stats[1][0], state.prev_top_domains_stats[1][0])

    prev_context = {
        'gov_diff': (gov_ca_diff, gov_ca_color, gov_ss_diff, gov_ss_color),
        'social_diff': (social_ca_diff, social_ca_color, social_ss_diff, social_ss_color),
        'top_diff': (top_ca_diff, top_ca_color, top_ss_diff, top_ss_color),
    }

    support_context = {
        'int': int,  # pass the int() function to the context
        'round': round  # pass the abs() function to the context
    }

    context.update(prev_context)
    context.update(support_context)

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
