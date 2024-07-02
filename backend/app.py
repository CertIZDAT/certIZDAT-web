import os
import sys
from datetime import date

from flask import Flask, request, render_template, send_file
from flask_sslify import SSLify

from utils.StatsState import StatsState
from utils.common import get_diff_and_color

sys.path.append("../")
from analyser.utils.cert_references import SELF_SIGNED_CERTS as ss_list

app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/', static_url_path='')

# Check if the DEBUG environment variable is set
app.config['DEBUG'] = os.environ.get('DEBUG')

if not app.config['DEBUG']:
    sslify = SSLify(app)

state = StatsState()
state.init_cache()


@app.route('/')
def index():
    state.update_cache(date.today())

    russian_trusted_ca_index = 0
    self_signed_index = 1

    gov_ca_count = \
        len(state.actual_government_domains_stats[russian_trusted_ca_index][0].split(',')) if \
        state.actual_government_domains_stats[russian_trusted_ca_index][0] else 0

    gov_ss_count = \
        len(state.actual_government_domains_stats[self_signed_index][0].split(',')) if \
        state.actual_government_domains_stats[self_signed_index][0] else 0

    social_ca_count = \
        len(state.actual_social_domains_stats[russian_trusted_ca_index][0].split(',')) if \
        state.actual_social_domains_stats[russian_trusted_ca_index][0] else 0

    social_ss_count = \
        len(state.actual_social_domains_stats[self_signed_index][0].split(',')) if \
        state.actual_social_domains_stats[self_signed_index][0] else 0

    top_ca_count = \
        len(state.actual_top_domains_stats[russian_trusted_ca_index][0].split(',')) if \
        state.actual_top_domains_stats[russian_trusted_ca_index][0] else 0

    top_ss_count = \
        len(state.actual_top_domains_stats[self_signed_index][0].split(',')) if \
        state.actual_top_domains_stats[self_signed_index][0] else 0

    context = {
        # Initial state for site_list is government sites with russian trusted CA
        'site_list': state.actual_government_domains_stats[russian_trusted_ca_index][0].replace(',', '\n'),
        'last_update_time': state.last_analysis_time,
        'actual_entries_count': state.actual_entries_count,
        'data_changed': state.data_changed,
        'gov_ca_count': gov_ca_count,
        'gov_ss_count': gov_ss_count,
        'social_ca_count': social_ca_count,
        'social_ss_count': social_ss_count,
        'top_ca_count': top_ca_count,
        'top_ss_count': top_ss_count
    }

    # FIXME: app crashed if no prev month in db

    # Get the government diffs
    if state.prev_government_domains_stats[russian_trusted_ca_index] is not None:
        gov_ca_diff, gov_ca_color = get_diff_and_color(
            state.actual_government_domains_stats[russian_trusted_ca_index][0],
            state.prev_government_domains_stats[russian_trusted_ca_index][0])
    else:
        gov_ca_diff, gov_ca_color = "0", "var(--main-green-color)"

    if state.prev_government_domains_stats[self_signed_index] is not None:
        gov_ss_diff, gov_ss_color = get_diff_and_color(
            state.actual_government_domains_stats[self_signed_index][0],
            state.prev_government_domains_stats[self_signed_index][0])
    else:
        gov_ss_diff, gov_ss_color = "0", "var(--main-green-color)"

    # Get the social diffs
    if state.prev_social_domains_stats[russian_trusted_ca_index] is not None:
        social_ca_diff, social_ca_color = get_diff_and_color(
            state.actual_social_domains_stats[russian_trusted_ca_index][0],
            state.prev_social_domains_stats[russian_trusted_ca_index][0])
    else:
      social_ca_diff, social_ca_color = "0", "var(--main-green-color)"

    if state.prev_social_domains_stats[self_signed_index] is not None:
        social_ss_diff, social_ss_color = get_diff_and_color(
            state.actual_social_domains_stats[self_signed_index][0],
            state.prev_social_domains_stats[self_signed_index][0])
    else:
        social_ss_diff, social_ss_color = "0", "var(--main-green-color)"

    # Get the top diffs
    if state.prev_top_domains_stats[russian_trusted_ca_index] is not None:
        top_ca_diff, top_ca_color = get_diff_and_color(
            state.actual_top_domains_stats[russian_trusted_ca_index][0],
            state.prev_top_domains_stats[russian_trusted_ca_index][0])
    else:
        top_ca_diff, top_ca_color = "0", "var(--main-green-color)"

    if state.prev_top_domains_stats[self_signed_index] is not None:
        top_ss_diff, top_ss_color = get_diff_and_color(
            state.actual_top_domains_stats[self_signed_index][0],
            state.prev_top_domains_stats[self_signed_index][0])
    else:
        top_ss_diff, top_ss_color = "0", "var(--main-green-color)"

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
    template_name = 'index.html' if app.config['DEBUG'] else 'index-min.html'
    return render_template(template_name, **context, app=app)


@app.route('/faq.html')
def faq_page():
    clean_res = ', '.join(i for i in ss_list)
    template_name = 'faq.html' if app.config['DEBUG'] else 'faq-min.html'
    return render_template(template_name, ss_list=clean_res, app=app)


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    requested_url = request.url
    print(f'404 error for URL: {requested_url}\nerror: {e}')
    template_name = '404.html' if app.config['DEBUG'] else '404-min.html'
    return render_template(template_name, app=app), 404


# Handle internal errors
@app.errorhandler(Exception)
def internal_error(e):
    print(f'Internal error: {e}')
    template_name = 'err.html' if app.config['DEBUG'] else 'err-min.html'
    return render_template(template_name, err_info=e)


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


if __name__ == '__main__':
    app.run()
