import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta

from utils import db


@dataclass
class StatsState:
    def __init__(self) -> None:
        self.cache_update_date: date = date.today()

    def __get_data_from_db(self):
        pass

    def init_cache(self):
        try:
            connection = db.get_db_connection(f'../analyser/statistics.db')
        except sqlite3.Error as e:
            pass
        self.__get_data_from_db()

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
