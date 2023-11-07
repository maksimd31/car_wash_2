# mybd.py
# устанавливаем MySQL на компьютере
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234qwer'

)

# создание курсора
cursorObject = dataBase.cursor()

# создание базы данных
cursorObject.execute("CREATE DATABASE dataMysql")

print('База данных создана')

"Таким образом мы создаем базу данных mysql"
