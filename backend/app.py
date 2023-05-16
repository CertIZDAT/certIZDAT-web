import os
from datetime import date
import sys

from flask import Flask, render_template, send_file

from utils.StatsState import StatsState
from utils.common import get_diff_and_color

sys.path.append("../")
from analyser.utils.web_consts import SELF_SIGNED_CERTS as ss_list

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
    top_ca_count = len(state.actual_top_domains_stats[0][0].split(
        ',')) if state.actual_top_domains_stats[0][0] else 0
    top_ss_count = len(state.actual_top_domains_stats[1][0].split(
        ',')) if state.actual_top_domains_stats[1][0] else 0

    context = {
        'site_list': state.actual_government_domains_stats[0][0].replace(',', '\n'),
        'last_update_time': state.last_analysis_time,
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


@app.route('/faq.html')
def faq_page():
    clean_res = ', '.join(i for i in ss_list)
    return render_template('faq.html', ss_list=clean_res)


@app.route('/download_dump')
def download_dump():
    file_path: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'analyser',
        'statistics.db')
    return send_file(file_path, as_attachment=True, mimetype='application/x-sqlite3')


# Government lists
@app.route('/process/gov-ca')
def gov_ca():
    return state.actual_government_domains_stats[0][0].replace(',', '\n')


@app.route('/process/gov-ss')
def gov_ss():
    return state.actual_government_domains_stats[1][0].replace(',', '\n')


# Social lists
@app.route('/process/social-ca')
def social_ca():
    return state.actual_social_domains_stats[0][0].replace(',', '\n')


@app.route('/process/social-ss')
def social_ss():
    return state.actual_social_domains_stats[1][0].replace(',', '\n')


# Top-100 lists
@app.route('/process/top-ca')
def top_ca():
    return state.actual_top_domains_stats[0][0].replace(',', '\n')


@app.route('/process/top-ss')
def top_ss():
    return state.actual_top_domains_stats[1][0].replace(',', '\n')


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    print(f'404 error: {e}')
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
