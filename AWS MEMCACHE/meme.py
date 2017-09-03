from flask import Flask,render_template,request,jsonify
import csv
import sys,os
import time
import random
import hashlib
import pymysql.cursors
import memcache

app = Flask(__name__)

#mysqlconn
dbconn=pymysql.connect(host=[HOSTNAME],user="root",
                  passwd=[PASSWORD],db=[DATABASENAME],port=3306,local_infile=True,charset='utf8'
                   ,cursorclass=pymysql.cursors.DictCursor)



#memcacheconn
memc = memcache.Client([memcacheid])

# beforeTime = time.time()
# print beforeTime
# query = memc.get('alldata')
#
# if not query:
#     cursor = dbconn.cursor()
#     cursor.execute('SELECT COUNT(*) FROM testdb.quiz;')
#     print 'count'
#     con = cursor.fetchall()
#     memc.set('alldata',con,1200)
#     print "Updated memcached with MySQL data"
# else:
#     print "Loaded data from memcached"
#     for row in query:
#         print "%s, %s" % (row[0], row[1])
#
# afterTime = time.time()
# print afterTime
#
# differenceTime=afterTime-beforeTime
# print differenceTime

@app.route('/')
def hello_world():
    return render_template('disp.html')

@app.route('/display',methods=['get'])
def display():
    beforeTime = time.time()
    print beforeTime
    query = memc.get('alldata')

    if not query:
        cursor = dbconn.cursor()
        cursor.execute('SELECT COUNT(*) FROM testdb.abc;')
        print 'count'
        con = cursor.fetchall()
        memc.set('alldata', con, 1200)
        print "Updated memcached with MySQL data"
    else:
        print "Loaded data from memcached"
        for row in query:
            print row

    afterTime = time.time()
    print afterTime

    differenceTime = afterTime - beforeTime
    print differenceTime
    return str(float(differenceTime))
@app.route('/ran',methods=['get'])
def rand():
    beforeTime = time.time()
    print beforeTime
    query = memc.get('fdata')
    cursor = dbconn.cursor()
    cursor.execute('SELECT COUNT(*) FROM testdb.abc;')
    print 'count'
    con = cursor.fetchall()
    count = len(con)
    beforeTime = time.time()
    for x in range(1, 5000):
                rand_number = random.randrange(0,count)
                sqlselect = "SELECT * FROM testdb.abc LIMIT {}".format(rand_number)
                query=memc.get('fdata'+str(x))
                if (query is None):
			status=cursor.execute(sqlselect)
			memc.set('fdata'+str(x),status,1200)
                        dbconn.commit()
    afterTime = time.time()
    print afterTime

    timeDifference = afterTime - beforeTime
    print timeDifference
    return str(float(timeDifference))

@app.route('/ranlimit',methods=['get'])
def randlim():
    beforeTime = time.time()
    print beforeTime
    query = memc.get('fdata')
    cursor = dbconn.cursor()
    cursor.execute('SELECT COUNT(*) FROM testdb.abc;')
    print 'count'
    con = cursor.fetchall()
    count = len(con)
    beforeTime = time.time()
    for x in range(1, 5000):
                rand_number = random.randrange(200,800)
                sqlselect = "SELECT * FROM testdb.abc WITH(INDEX(inx)) LIMIT {} ".format(rand_number)
                query=memc.get('fdata'+str(x))
                if (query is None):
			status=cursor.execute(sqlselect)
			memc.set('fdata'+str(x),status,1200)
                        dbconn.commit()
    afterTime = time.time()
    print afterTime

    timeDifference = afterTime - beforeTime
    print timeDifference
    return str(float(timeDifference))


port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
