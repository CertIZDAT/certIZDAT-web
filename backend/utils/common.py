from utils import db


def __clean_db_response(response):
    items = [item.strip() for item in str(response).split(",")]
    return "\n".join([str(item[0]).strip("(),") if isinstance(item, tuple) and len(item) == 1 else item.split(' ')[0] for item in items])


def get_latest_counts(connection, type='CA'):
    # Get counts for CA and self-signed
    if type == 'CA':
        return int(__clean_db_response(connection.execute(
            db.get_last_ca_count_query).fetchall()[0][0]))
    else:
        return int(__clean_db_response(connection.execute(
            db.get_last_self_sign_count_query).fetchall()[0][0])


def get_latest_list_results(connection, type='CA'):
    # Get list of CA and self-signed
    if type == 'CA':
        return __clean_db_response(connection.execute(
            db.get_last_ca_list).fetchall()[0][0])
    else:
        return __clean_db_response(connection.execute(
            db.get_last_self_sign_list).fetchall()[0][0])


def get_last_update_time(connection):
    return connection.execute(
        db.get_last_update_date_time).fetchall()[0][0]


def get_total_dataset_size(connection):
    return connection.execute(
        db.get_dataset_size).fetchall()[0][0]
