from flask import Flask,render_template,request,jsonify
import pymysql.cursors
import os
import csv
import time
import random


import sys
app = Flask(__name__)

db=pymysql.connect(host="dbinspooja.czd77famuj50.us-east-2.rds.amazonaws.com",user="root",
                  passwd="",db="testdb",port=3306,local_infile=True,charset='utf8'
                   ,cursorclass=pymysql.cursors.DictCursor)



@app.route('/')
def hello_world():
    return render_template('dbview.html')

@app.route('/createtable',methods=['post'])
def createdb():
    cursor=db.cursor()
    filename = 'C:/Users/Administrators/Desktop/uc.csv'
    tablename='abc'
    droptbl = "DROP TABLE IF EXISTS testdb.quiz;"
    cursor.execute(droptbl)

    #createtale
    create = """Create table IF NOT EXISTS testdb.abc(IPEDSID varchar(100) DEFAULT NULL,NAME varchar(100) DEFAULT NULL,
    ADDRESS varchar(100) DEFAULT NULL,CITY varchar(100) DEFAULT NULL,STATE varchar(100) DEFAULT NULL,ZIP varchar(100) DEFAULT NULL,
    TELEPHONE varchar(100) DEFAULT NULL,POPULATION varchar(100) DEFAULT NULL,COUNTY varchar(100) DEFAULT NULL,
    COUNTYFIPS varchar(100) DEFAULT NULL,LATITUDE varchar(100) DEFAULT NULL,LONGITUDE varchar(100) DEFAULT NULL,
    ALIAS varchar(100) DEFAULT NULL,TOT_ENROLL varchar(100) DEFAULT NULL,DORM_CAP varchar(100) DEFAULT NULL,TOT_EMPLOY varchar(100) DEFAULT NULL)"""
    cursor.execute(create)
    print create
    db.commit()
    

    print 'indexed'
    db.commit()
    #insert
    #rowreader = csv.reader('C:/Users/Administrators/Desktop/week.csv', delimiter=',', quotechar='`')
    #print rowreader
    insert="""LOAD DATA LOCAL INFILE 'C:/Users/Administrator/Desktop/aws2/uc.csv' INTO TABLE abc 
             FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'LINES TERMINATED BY '\n' IGNORE 1 LINES"""
    cursor.execute(insert)
    print 'inserted'

    db.commit()

    #altertableindex
    #cursor.execute('CREATE INDEX inx ON testdb.quiz(IPEDSID);')

    #indexin="""ALTER TABLE quiz ADD INDEX ind (IPEDSID)"""
    #cursor.execute(indexin);
    
    
    return render_template('dbview.html')

@app.route('/querydisplay',methods=['post'])
def querydb():
    
    cursor=db.cursor()
    

    #insert
    text1 = request.form.get('text1')
    text2 = request.form.get('text2')
    text3 = request.form.get('text3')
    #cursor.execute('SELECT COUNT(IPEDSID) FROM testdb.earthquakeweek1 where LATITUDE between '
    #          +text1+' and '+text2+' and place like \'%'+text3+'\' collate utf8_bin;')
    #cursor.execute('select ALIAS from testdb.quiz where CITY like \'%'+text1+'\' collate utf8_bin OR STATE like \'%'+text2+'\' collate utf8_bin AND 'text3'=MIN(TOT_ENROLL);')
    res=cursor.fetchall()
    return render_template('res.html',result=res)
@app.route('/count',methods=['post'])
def query():
    cursor=db.cursor()
    cursor.execute('SELECT COUNT(*) FROM testdb.abc;')
    print 'count'
    con=cursor.fetchall()
    db.commit()
    
    return render_template('count.html',con=con)

@app.route('/abc', methods=['GET'])
def cal_memc():
   cursor = db.cursor()
   beforeTime = time.time()
   print beforeTime
   for x in range(1, 500):
            rand_number = random.randrange(200,300)
            print(rand_number)
            sqlselect ="SELECT * FROM testdb.abc WHERE ALIAS LIKE '%N' LIMIT {} ".format(rand_number)
            cursor.execute(sqlselect)
            count_res = cursor.fetchall()
   afterTime = time.time()
   print afterTime
   timeDifference = afterTime - beforeTime
   print timeDifference
   return str(float(timeDifference))



port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=int(port))
