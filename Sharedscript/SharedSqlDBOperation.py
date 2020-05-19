#!/usr/bin/python3
# -*- coding: utf-8 -*-
import shutil
import sqlite3
from prettytable import PrettyTable

class ConnSql(object):
    def __init__(self, file):
        self.__file = file
        self.sql_conn = sqlite3.connect(self.__file)
        print("info: read database successfully！")

    def execute_command(self, sql):
        cursor = self.sql_conn.cursor()
        cursor = cursor.execute(sql)
        return cursor

    @staticmethod
    def print_table(cursor):
        table = PrettyTable(['id', 'user_id', 'feature_base64'])
        index = 1
        for row in cursor:
            table.add_row([index, str(row[2]), str(row[13])])
            index = index + 1
        print(table)

    @staticmethod
    def write_file(remote, cursor, log_file):
        with open(log_file, 'w') as file:
            for row in cursor:
                file.write(remote + str(row[13]) + ".jpg\n")

    def disconnect(self):
        self.sql_conn.close()


if __name__ == '__main__':
    sql_conn = ConnSql('D:\\test-project\\006-PassC\\feature_db.sqlite')
    result = sql_conn.execute_command('select * from feature_table')
    print(result)
    print(list(result))
    # sql_conn.print_table(result)