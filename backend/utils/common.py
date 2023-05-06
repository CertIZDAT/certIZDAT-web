from utils import db


def get_latest_list_results(connection, ssl_case: str = 'CA') -> str:
    # Get list of CA and self-signed
    if ssl_case == 'CA':
        return __clean_db_response(connection.execute(
            db.get_last_ca_list).fetchall()[0][0])
    else:
        response = connection.execute(
            db.get_last_self_sign_list).fetchall()[0][0]
        items = [item.strip() for item in str(response).split(",")]
        return "\n".join([item for item in items])


def __clean_db_response(response) -> str:
    items = [item.strip() for item in str(response).split(",")]
    return "\n".join(
        [str(item[0]).strip("(),") if isinstance(item, tuple) and len(item) == 1 else item.split(' ')[0] for item in
         items])
