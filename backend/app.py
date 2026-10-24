import os
import sys
from datetime import date

from flask import Flask, Response, abort, redirect, render_template, request, send_file
from utils.common import get_diff_and_color
from utils.StatsState import StatsState
from werkzeug.exceptions import HTTPException

sys.path.append("../")
from analyser.utils.cert_references import SELF_SIGNED_CERTS as ss_list

app = Flask(
    __name__,
    template_folder="../frontend/",
    static_folder="../frontend/static/",
    static_url_path="",
)


def environment_flag(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    if value not in {"", "0", "false", "no", "off", "1", "true", "yes", "on"}:
        raise ValueError(f"{name} must be a boolean value")
    return value in {"1", "true", "yes", "on"}


app.config["DEBUG"] = environment_flag("DEBUG")
app.config["ENFORCE_HTTPS"] = not environment_flag("ALLOW_INSECURE_HTTP")
app.config["TRUSTED_HOSTS"] = None if app.config["DEBUG"] else ["certizdat.org"]


@app.before_request
def enforce_https():
    # Only the WSGI server may establish the scheme; never trust raw proxy headers.
    if app.config["ENFORCE_HTTPS"] and not request.is_secure:
        return redirect(request.url.replace("http://", "https://", 1), code=308)


@app.after_request
def security_headers(response: Response) -> Response:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.bunny.net; "
        "font-src 'self' https://fonts.bunny.net; img-src 'self'; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
    )
    if request.is_secure:
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response


state = StatsState()
state.init_cache()


@app.route("/")
def index():
    state.update_cache(date.today())

    russian_trusted_ca_index = 0
    self_signed_index = 1

    gov_ca_count = (
        len(
            state.actual_government_domains_stats[russian_trusted_ca_index][0].split(
                ","
            )
        )
        if state.actual_government_domains_stats[russian_trusted_ca_index][0]
        else 0
    )

    gov_ss_count = (
        len(state.actual_government_domains_stats[self_signed_index][0].split(","))
        if state.actual_government_domains_stats[self_signed_index][0]
        else 0
    )

    social_ca_count = (
        len(state.actual_social_domains_stats[russian_trusted_ca_index][0].split(","))
        if state.actual_social_domains_stats[russian_trusted_ca_index][0]
        else 0
    )

    social_ss_count = (
        len(state.actual_social_domains_stats[self_signed_index][0].split(","))
        if state.actual_social_domains_stats[self_signed_index][0]
        else 0
    )

    top_ca_count = (
        len(state.actual_top_domains_stats[russian_trusted_ca_index][0].split(","))
        if state.actual_top_domains_stats[russian_trusted_ca_index][0]
        else 0
    )

    top_ss_count = (
        len(state.actual_top_domains_stats[self_signed_index][0].split(","))
        if state.actual_top_domains_stats[self_signed_index][0]
        else 0
    )

    context = {
        # Initial state for site_list is government sites with russian trusted CA
        "site_list": state.actual_government_domains_stats[russian_trusted_ca_index][
            0
        ].replace(",", "\n"),
        "last_update_time": state.last_analysis_time,
        "actual_entries_count": state.actual_entries_count,
        "data_changed": state.data_changed,
        "gov_ca_count": gov_ca_count,
        "gov_ss_count": gov_ss_count,
        "social_ca_count": social_ca_count,
        "social_ss_count": social_ss_count,
        "top_ca_count": top_ca_count,
        "top_ss_count": top_ss_count,
    }

    # FIXME: app crashed if no prev month in db

    # Get the government diffs
    if state.prev_government_domains_stats[russian_trusted_ca_index] is not None:
        gov_ca_diff, gov_ca_color = get_diff_and_color(
            state.actual_government_domains_stats[russian_trusted_ca_index][0],
            state.prev_government_domains_stats[russian_trusted_ca_index][0],
        )
    else:
        gov_ca_diff, gov_ca_color = "0", "var(--main-green-color)"

    if state.prev_government_domains_stats[self_signed_index] is not None:
        gov_ss_diff, gov_ss_color = get_diff_and_color(
            state.actual_government_domains_stats[self_signed_index][0],
            state.prev_government_domains_stats[self_signed_index][0],
        )
    else:
        gov_ss_diff, gov_ss_color = "0", "var(--main-green-color)"

    # Get the social diffs
    if state.prev_social_domains_stats[russian_trusted_ca_index] is not None:
        social_ca_diff, social_ca_color = get_diff_and_color(
            state.actual_social_domains_stats[russian_trusted_ca_index][0],
            state.prev_social_domains_stats[russian_trusted_ca_index][0],
        )
    else:
        social_ca_diff, social_ca_color = "0", "var(--main-green-color)"

    if state.prev_social_domains_stats[self_signed_index] is not None:
        social_ss_diff, social_ss_color = get_diff_and_color(
            state.actual_social_domains_stats[self_signed_index][0],
            state.prev_social_domains_stats[self_signed_index][0],
        )
    else:
        social_ss_diff, social_ss_color = "0", "var(--main-green-color)"

    # Get the top diffs
    if state.prev_top_domains_stats[russian_trusted_ca_index] is not None:
        top_ca_diff, top_ca_color = get_diff_and_color(
            state.actual_top_domains_stats[russian_trusted_ca_index][0],
            state.prev_top_domains_stats[russian_trusted_ca_index][0],
        )
    else:
        top_ca_diff, top_ca_color = "0", "var(--main-green-color)"

    if state.prev_top_domains_stats[self_signed_index] is not None:
        top_ss_diff, top_ss_color = get_diff_and_color(
            state.actual_top_domains_stats[self_signed_index][0],
            state.prev_top_domains_stats[self_signed_index][0],
        )
    else:
        top_ss_diff, top_ss_color = "0", "var(--main-green-color)"

    prev_context = {
        "gov_diff": (gov_ca_diff, gov_ca_color, gov_ss_diff, gov_ss_color),
        "social_diff": (
            social_ca_diff,
            social_ca_color,
            social_ss_diff,
            social_ss_color,
        ),
        "top_diff": (top_ca_diff, top_ca_color, top_ss_diff, top_ss_color),
    }

    support_context = {
        "int": int,  # pass the int() function to the context
        "round": round,  # pass the abs() function to the context
    }

    context.update(prev_context)
    context.update(support_context)
    return render_template("index.html", **context)


@app.route("/faq.html")
def faq_page():
    clean_res = ", ".join(i for i in ss_list)
    return render_template("faq.html", ss_list=clean_res)


# 404 page
@app.errorhandler(404)
def page_not_found(e: HTTPException):
    return render_template("404.html"), 404


# Handle internal errors
@app.errorhandler(Exception)
def internal_error(e: Exception):
    if isinstance(e, HTTPException):
        return e
    app.logger.exception("Unhandled request error")
    return render_template("err.html"), 500


@app.route("/download_dump")
def download_dump():
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "analyser", "statistics.db"
    )
    try:
        return send_file(
            file_path,
            as_attachment=True,
            download_name="statistics.db",
            mimetype="application/x-sqlite3",
        )
    except (FileNotFoundError, IsADirectoryError):
        abort(503, description="The statistics database is unavailable.")


# Government lists
@app.route("/process/gov-ca")
def gov_ca():
    return Response(
        state.actual_government_domains_stats[0][0].replace(",", "\n"),
        mimetype="text/plain",
    )


@app.route("/process/gov-ss")
def gov_ss():
    return Response(
        state.actual_government_domains_stats[1][0].replace(",", "\n"),
        mimetype="text/plain",
    )


# Social lists
@app.route("/process/social-ca")
def social_ca():
    return Response(
        state.actual_social_domains_stats[0][0].replace(",", "\n"),
        mimetype="text/plain",
    )


@app.route("/process/social-ss")
def social_ss():
    return Response(
        state.actual_social_domains_stats[1][0].replace(",", "\n"),
        mimetype="text/plain",
    )


# Top-100 lists
@app.route("/process/top-ca")
def top_ca():
    return Response(
        state.actual_top_domains_stats[0][0].replace(",", "\n"),
        mimetype="text/plain",
    )


@app.route("/process/top-ss")
def top_ss():
    return Response(
        state.actual_top_domains_stats[1][0].replace(",", "\n"),
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.run()
