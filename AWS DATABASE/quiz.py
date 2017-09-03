from flask import Flask,render_template,request,jsonify
import MySQLdb
import pymysql.cursors

import time
import hashlib
import json
import csv
from random import randint
import sys
app = Flask(__name__)

db=pymysql.connect(host=[host name],user="root",
                  passwd=[password],db=[databasenme],port=3306,local_infile=True,charset='utf8mb4'
                   ,cursorclass=pymysql.cursors.DictCursor)
dbname = 'testdb'
tablename = 'quiz'


file_name  = 'C:\Users\Pooja\Downloads\uc.csv'
f_obj = open(file_name, 'r')
reader = csv.reader(f_obj)
headers = next(reader, None)
print (headers)
cursor = db.cursor()

create_query = 'Create table IF NOT EXISTS '+dbname+'.'+tablename+' ( '
for heading in headers:
	create_query +=  heading + " varchar(100) DEFAULT NULL,"

create_query = create_query[:-1]
create_query += ")"
print (create_query)

cursor.execute(create_query)
print('Table Created')

