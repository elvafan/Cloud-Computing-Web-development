import mysql.connector
from datetime import datetime

from Front import dbconfig


class ServerDb:

    def __init__(self):
        self.db = mysql.connector.connect(user=dbconfig.db_config['user'],
                                       password=dbconfig.db_config['password'],
                                       host=dbconfig.db_config['host'],
                                       database=dbconfig.db_config['database'])

    def update_configure(self, policy, capacity=-1):
        cursor = self.db.cursor()
        if capacity != -1:
            query = '''UPDATE `serverdb`.`configure` SET replacement_policy = %s, capacity = %s WHERE id = 0;'''
            cursor.execute(query, (policy, capacity))
        else:
            query = '''UPDATE `serverdb`.`configure` SET replacement_policy = %s, capacity = capacity WHERE id = 0;'''
            cursor.execute(query, (policy,))
        self.db.commit()

    def insert_image(self, key, name):
        cursor = self.db.cursor(buffered=True)
        query = '''SELECT * FROM `serverdb`.`item` WHERE `key` = %s;'''
        cursor.execute(query, (key,))
        now = datetime.now()
        if cursor.rowcount == 0:
            # No collision
            query = '''INSERT INTO `serverdb`.`item` (`key`, `name`, `LAT`) VALUES (%s, %s, %s);'''
            cursor.execute(query, (key, name, now,))
        else:
            # Collision, replace old img name with new name
            query = '''UPDATE `serverdb`.`item` SET `name` = %s, `LAT` = %s WHERE `key` = %s;'''
            cursor.execute(query, (name, now, key,))

        self.db.commit()

    def read_image(self, key):
        cursor = self.db.cursor(buffered=True)
        query = '''SELECT `name` FROM `serverdb`.`item` WHERE `key` = %s;'''
        cursor.execute(query, (key,))

        if cursor.rowcount == 0:
            return -1
        else:
            result = cursor.fetchone()
            print(result)
            # Update Last accessed time
            now = datetime.now()
            query = '''UPDATE `serverdb`.`item` SET `name` = %s, `LAT` = %s WHERE `key` = %s;'''
            cursor.execute(query, (result[0], now, key,))
            self.db.commit()
            return result[0]

    def read_all_keys(self):
        cursor = self.db.cursor(buffered=True)
        query = '''SELECT `key` FROM `serverdb`.`item`;'''
        cursor.execute(query)
        results = cursor.fetchall()
        ret = []
        for i in results:
            ret.append(i[0])

        return ret

    def read_past_10min_stats(self):
        cursor = self.db.cursor(buffered=True)
        query = '''SELECT * FROM `serverdb`.`stats` WHERE `time` >= NOW() - INTERVAL 10 MINUTE;'''
        cursor.execute(query)
        results = cursor.fetchall()

        time_added = []
        items_in_cache = []
        total_size = []
        n_requests_served = []
        n_requests_missed = []

        for i in results:
            time_added.append(i[0])
            items_in_cache.append(i[1])
            total_size.append(i[2])
            n_requests_served.append(i[3])
            n_requests_missed.append(i[4])

        return time_added, items_in_cache, total_size, n_requests_served, n_requests_missed



