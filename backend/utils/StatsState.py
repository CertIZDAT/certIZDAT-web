import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from sqlite3 import Connection

from utils import db


@dataclass
class StatsState:
    def __init__(self) -> None:
        self.cache_update_date: date = date.today()
        # This field contains the count of entries in each category (gov, social, top-100)
        # for the last available date-time in the database.
        self.actual_entries_count: tuple[int, int, int]
        # List of the government associated sites what require a Russian Trusted CA or self-signed certificate
        # issued by the Russian government.
        self.actual_government_domains_stats: tuple[str, str]
        # List of the social important sites what require a Russian Trusted CA or self-signed certificate
        # issued by the Russian government.
        self.actual_social_domains_stats: tuple[str, str]
        # List of the top-100 sites by popularity what require a Russian Trusted CA or self-signed certificate
        # issued by the Russian government.
        self.actual_top_domains_stats: tuple[str, str]

        # Statistics for the previous month. If there are no previous records then last available results will be used.
        self.prev_entries_count: tuple[int, int, int]
        self.prev_government_domains_stats: tuple[str, str]
        self.prev_social_domains_stats: tuple[str, str]
        self.prev_top_domains_stats: tuple[str, str]

    def __get_data_from_db(self, connection: Connection):
        pass

    def init_cache(self):
        try:
            connection = db.get_db_connection(f'../analyser/statistics.db')
            self.__get_data_from_db(connection)
        except sqlite3.Error as e:
            print(f'get db connection error: {e}')
        finally:
            if 'connection' in locals():
                connection.close()

    def update_cache(self, current_date: date) -> None:
        outdated_interval = timedelta(days=7)
        diff = current_date - self.cache_update_date
        if diff >= outdated_interval:
            self.cache_update_date = current_date

            try:
                connection = db.get_db_connection(f'../analyser/statistics.db')
            except sqlite3.Error as e:
                pass
            self.__get_data_from_db()
