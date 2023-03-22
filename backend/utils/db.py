import sqlite3

get_all_ca_count_array = 'SELECT trusted_ca_count FROM statistic_table;'

get_last_ca_count_query = 'SELECT trusted_ca_count FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
get_last_self_sign_count_query = 'SELECT self_signed_count FROM statistic_table ORDER BY date_time DESC LIMIT 1;'

get_last_ca_list = 'SELECT list_of_trusted_ca FROM statistic_table ORDER BY date_time DESC LIMIT 1;'
get_last_self_sign_list = 'SELECT list_of_self_sign FROM statistic_table ORDER BY date_time DESC LIMIT 1;'


def get_db_connection(db_name):
    connect = sqlite3.connect(db_name)
    return connect

# get results from db:
#   list of the CA
#   list of the self-signed
# Note: get results at select change

# get CA count from db
#   send results to JS plotter
