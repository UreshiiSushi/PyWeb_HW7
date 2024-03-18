import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# CREATE DATABASE university
connection = psycopg2.connect(user="postgres", password="1234Qwe")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
sql_create_database = "create database university"
cursor.execute(sql_create_database)
cursor.close()
connection.close()