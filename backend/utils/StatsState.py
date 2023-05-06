import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from sqlite3 import Connection

from utils import db


@dataclass
class StatsState:
    def __init__(self) -> None:
        self.cache_update_date: date = date.today()

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
