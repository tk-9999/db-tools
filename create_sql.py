# 各テーブルの SQL ファイル を生成する
import mysql.connector
import json
import re
import pathlib
import os

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def read_setting():
    json_open = open('setting.json', 'r')
    return json.load(json_open)['create_sql']

setting = read_setting()

# DB 接続の設定をする
db_connect = mysql.connector.connect(
    host=setting["host"],
    port=setting["port"],
    user=setting["user"],
    password=setting["password"]
)

db_curs = db_connect.cursor()


for database in setting['databases']:
    db_curs.execute('USE ' + database)
    db_curs.execute('SHOW TABLES')
    sql_file_path = pathlib.Path('SQL_FILE\\' + database)
    makedirs(sql_file_path)

    for table in db_curs.fetchall():
        db_curs.execute('DESCRIBE ' + table[0])
        column_name_list = ",".join([x[0] for x in db_curs.fetchall()])

        sql_file = pathlib.Path(str(sql_file_path) + '\\' + table[0] + '.sql')
        with sql_file.open(mode='w') as f:
            f.write('SELECT ' + column_name_list + ' FROM ' + table[0])

db_connect.close()




