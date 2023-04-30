import sqlite3
from sqlite3 import Connection

get_row_count: str = 'SELECT COUNT(*) FROM statistic_table;'

# Get list of the government associated sites that use Russian Trusted CA/self-signed certificates
gov_get_last_ca_list: str = 'SELECT gov_ca_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
gov_get_last_ss_list: str = 'SELECT gov_ss_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

# Get list of the social sites that use Russian Trusted CA/self-signed certificates
social_get_last_ca_list: str = 'SELECT social_ca_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
social_get_last_ss_list: str = 'SELECT social_ss_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

# Get list of the top-100 runet sites that use Russian Trusted CA/self-signed certificates
top_get_last_ca_list: str = 'SELECT top_ca_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
top_get_last_ss_list: str = 'SELECT top_ss_list FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

# TODO: Try to get stats with f'' strings. Passing: ('gov','last)/('gov','prev')...
get_gov_stats_for_last_month: str = 'SELECT gov_ca_list, gov_ss_list, gov_other_ssl_err_list ' \
                                    'FROM statistic_table ' \
                                    'WHERE date_time = (SELECT MAX(date_time) FROM statistic_table);'

# If there is no data available for the previous month, the query returns the data with the latest date_time.
get_gov_stats_for_prev_month: str = 'SELECT gov_ca_list, gov_ss_list, gov_other_ssl_err_list ' \
                                    'FROM statistic_table' \
                                    'WHERE strftime(\'%Y-%m\', date_time) = strftime(\'%Y-%m\', date(\'now\', ' \
                                    '\'-1 month\'))' \
                                    'OR (SELECT MAX(strftime(\'%Y-%m\', date_time)) ' \
                                    'FROM statistic_table) < strftime(\'%Y-%m\', date(\'now\', \'-1 month\'))' \
                                    'ORDER BY date_time DESC' \
                                    'LIMIT 1;'


def get_db_connection(db_name: str) -> Connection:
    connect = sqlite3.connect(db_name)
    return connect
