import sqlite3
from sqlite3 import Connection


# Get list of the government/social/top sites that use Russian Trusted CA/self-signed certificates
def get_list_of(category: str, ssl_case: str, time: str) -> str:
    if category in ['gov', 'social', 'top'] and ssl_case in ['ca', 'ss'] and time in ['now', 'prev']:
        if time == 'now':
            return f'SELECT {category}_{ssl_case}_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
        elif time == 'prev':
            return f'SELECT {category}_{ssl_case}_list FROM statistic_table ' \
                   'WHERE strftime(\'%Y-%m\', date_time) = strftime(\'%Y-%m\', date(\'now\', ' \
                   '\'-1 month\')) ' \
                   'OR (SELECT MAX(strftime(\'%Y-%m\', date_time)) ' \
                   'FROM statistic_table) < strftime(\'%Y-%m\', date(\'now\', \'-1 month\')) ' \
                   'ORDER BY date_time DESC ' \
                   'LIMIT 1;'
    print(f'ERROR: error in get_list_of – category: {category}, ssl_case: {ssl_case}')
    exit(1)


# Get total count of all government/social/top sites
def get_stats_count(category: str, time: str) -> str:
    if category in ['gov', 'social', 'top'] and time in ['now', 'prev']:
        if time == 'now':
            return f'SELECT {category}_count ' \
                   'FROM statistic_table ' \
                   'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'
        elif time == 'prev':
            return f'SELECT {category}_count ' \
                   'FROM statistic_table ' \
                   'WHERE strftime(\'%Y-%m\', date_time) = strftime(\'%Y-%m\', date(\'now\', ' \
                   '\'-1 month\')) ' \
                   'OR (SELECT MAX(strftime(\'%Y-%m\', date_time)) ' \
                   'FROM statistic_table) < strftime(\'%Y-%m\', date(\'now\', \'-1 month\')) ' \
                   'ORDER BY date_time DESC ' \
                   'LIMIT 1;'
    print(f'ERROR: error in get_stats_count – category: {category}, time: {time}')
    exit(1)


def get_last_update_time():
    return f'SELECT date_time ' \
           'FROM statistic_table ' \
           'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'

def is_data_changed():
    return f'SELECT is_dataset_updated ' \
           'FROM statistic_table ' \
           'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'


def get_db_connection(db_name: str) -> Connection:
    connect = sqlite3.connect(db_name)
    return connect
