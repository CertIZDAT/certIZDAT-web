import sqlite3

# List of possible queries
get_all_ca_count_array = 'SELECT trusted_ca_count FROM statistic_table;'

get_last_ca_count_query = 'SELECT trusted_ca_count FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
get_last_self_sign_count_query = 'SELECT self_signed_count FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

get_last_ca_list = 'SELECT list_of_trusted_ca FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
get_last_self_sign_list = 'SELECT list_of_self_sign FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

get_last_update_date_time = 'SELECT date_time FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

get_dataset_size = 'SELECT total_ds_size FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

get_ca_count_for_last_month = 'SELECT trusted_ca_count from statistic_table WHERE date(date_time) >= date(\'now\', \'-1 month\')'
get_dates_for_last_month = 'SELECT date(date_time) AS date_only FROM statistic_table WHERE date(date_time) >= date(\'now\', \'-1 month\')'


def get_db_connection(db_name):
    connect = sqlite3.connect(db_name)
    return connect
