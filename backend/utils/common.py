from sqlite3 import Connection

from utils import db


def get_total_stats(connection: Connection):
    gov_stats: tuple[str] = connection.execute(db.get_gov_stats_for_last_month).fetchone()
    social_stats: tuple[str] = connection.execute(db.get_gov_stats_for_last_month).fetchone()
    top_stats: tuple[str] = connection.execute(db.get_gov_stats_for_last_month).fetchone()

    if connection.execute(db.get_row_count).fetchone() >= 2:
        gov_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()
        social_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()
        top_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()


def get_latest_list_results(connection, type='CA'):
    # Get list of CA and self-signed
    if type == 'CA':
        return __clean_db_response(connection.execute(
            db.get_last_ca_list).fetchall()[0][0])
    else:
        response = connection.execute(
            db.get_last_self_sign_list).fetchall()[0][0]
        items = [item.strip() for item in str(response).split(",")]
        return "\n".join([item for item in items])


def __clean_db_response(response):
    items = [item.strip() for item in str(response).split(",")]
    return "\n".join(
        [str(item[0]).strip("(),") if isinstance(item, tuple) and len(item) == 1 else item.split(' ')[0] for item in
         items])
