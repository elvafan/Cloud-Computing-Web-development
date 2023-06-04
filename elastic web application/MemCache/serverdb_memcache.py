import mysql.connector
from datetime import datetime

from MemCache import dbconfig


class ServerDb:

    def __init__(self):
        self.db = mysql.connector.connect(user=dbconfig.db_config['user'],
                                       password=dbconfig.db_config['password'],
                                       host=dbconfig.db_config['host'],
                                       database=dbconfig.db_config['database'])

    def add_stat(self, current_time, items_in_cache, total_size, n_requests_served, n_requests_missed):
        cursor = self.db.cursor()
        query = '''INSERT INTO serverdb.stats 
                        (`time`, `items_in_cache`, `total_size`, `n_requests_served`, `n_requests_missed`) 
                        VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (current_time, items_in_cache, total_size, n_requests_served, n_requests_missed))
        self.db.commit()

    def read_config(self):
        cursor = self.db.cursor()
        query = '''SELECT `replacement_policy`, `capacity` FROM serverdb.configure WHERE `id`=0;'''
        cursor.execute(query)
        results = cursor.fetchone()
        policy = results[0]
        capacity = results[1]
        return policy, capacity





