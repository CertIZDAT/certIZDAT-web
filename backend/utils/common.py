from utils import db


def get_diff_and_color(actual_value: str, prev_value: str):
    actual_domains: list[str] = actual_value.split(",")
    prev_domains: list[str] = prev_value.split(",")
    diff: int = len(actual_domains) - len(prev_domains)
    diff_str: str = f"+{diff}" if diff > 0 else str(diff)
    color: str = "green" if diff_str.startswith("-") or diff_str[0].isdigit() else "red"
    return diff_str, color


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
