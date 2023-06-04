import mysql.connector
from Front import dbconfig
from ManagerApp import ec2_pool

class ServerDb:

    def __init__(self):
        self.db = mysql.connector.connect(user=dbconfig.db_config['user'],
                                       password=dbconfig.db_config['password'],
                                       host=dbconfig.db_config['host'],
                                       database=dbconfig.db_config['database'])

    def update_a1_config(self, policy, capacity=-1):
        cursor = self.db.cursor()
        # Update the pool policy
        ec2_pool.policy = policy
        if capacity != -1:
            query = '''UPDATE `serverdb`.`configure` SET replacement_policy = %s, capacity = %s WHERE id = 0;'''
            cursor.execute(query, (policy, capacity))
        else:
            query = '''UPDATE `serverdb`.`configure` SET replacement_policy = %s, capacity = capacity WHERE id = 0;'''
            cursor.execute(query, (policy,))
        self.db.commit()

    def update_configure_autoscaler(self, config_name, config_value):
        
        if config_value == "":
            print(config_name, "None, no need to update")
        else:
            cursor = self.db.cursor()
            print(config_name,":", config_value)
            query = '''UPDATE `serverdb`.`configure` SET {0} = %s WHERE id = 0;'''.format(config_name)
            cursor.execute(query, (config_value,))
            self.db.commit()

    def clear_all_image_data(self):
        cursor = self.db.cursor()
        print("Rua")
        query = '''DELETE FROM `serverdb`.`item`;'''
        cursor.execute(query, ())
        self.db.commit()

    def read_as_config(self):
        cursor = self.db.cursor(buffered=True)
        query = '''SELECT * FROM `serverdb`.`configure`;'''
        cursor.execute(query)
        results = cursor.fetchall()

        for i in results:
            max_miss_rate = i[3]
            min_miss_rate = i[4]
            expand_ratio = i[5]
            shrink_ratio = i[6]

        return [max_miss_rate, min_miss_rate, expand_ratio, shrink_ratio]

