import sqlite3
from sqlite3 import Connection


# Get list of the government/social/top sites that use Russian Trusted CA/self-signed certificates
def get_list_of(category: str, ssl_case: str) -> str:
    if category in ['gov', 'social', 'top'] and ssl_case in ['ca', 'ss']:
        return f'SELECT {category}_{ssl_case}_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
    print(f'ERROR: error in get_list_of – category: {category}, ssl_case: {ssl_case}')
    exit(1)


# Get total count of all government/social/top sites
def get_stats_count(category: str, time: str) -> str:
    if category in ['gov', 'social', 'top'] and time in ['now', 'prev']:
        if time == 'now':
            return f'SELECT {category}_count' \
                   'FROM statistic_table' \
                   'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'
        else:
            return f'SELECT {category}_count' \
                   'FROM statistic_table' \
                   'WHERE strftime(\'%Y-%m\', date_time) = strftime(\'%Y-%m\', date(\'now\', ' \
                   '\'-1 month\'))' \
                   'OR (SELECT MAX(strftime(\'%Y-%m\', date_time)) ' \
                   'FROM statistic_table) < strftime(\'%Y-%m\', date(\'now\', \'-1 month\'))' \
                   'ORDER BY date_time DESC' \
                   'LIMIT 1;'
    print(f'ERROR: error in get_stats_count – category: {category}, time: {time}')
    exit(1)


def get_month_stats(category: str, time: str) -> str:
    if category in ['gov', 'social', 'top'] and time in ['now', 'prev']:
        if time == 'now':
            return f'SELECT {category}_ca_list, {category}_ss_list, {category}_other_ssl_err_list ' \
                   'FROM statistic_table ' \
                   'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'
        else:
            return f'SELECT {category}_ca_list, {category}_ss_list, {category}_other_ssl_err_list ' \
                   'FROM statistic_table' \
                   'WHERE strftime(\'%Y-%m\', date_time) = strftime(\'%Y-%m\', date(\'now\', ' \
                   '\'-1 month\'))' \
                   'OR (SELECT MAX(strftime(\'%Y-%m\', date_time)) ' \
                   'FROM statistic_table) < strftime(\'%Y-%m\', date(\'now\', \'-1 month\'))' \
                   'ORDER BY date_time DESC' \
                   'LIMIT 1;'
    print(f'ERROR: error in get_stats_count – category: {category}, time: {time}')
    exit(1)


def get_db_connection(db_name: str) -> Connection:
    connect = sqlite3.connect(db_name)
    return connect
