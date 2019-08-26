# Written on 24/08/19
# Author: Aneesh PA
# creates a MySQL database if it doesnt exist
# Checked on Windows10 64-bit, python 2.7, openopc, mysql-connector-python
# Reads from 'pushdb' database
# Tables 'push_time' contains oven_no and push_time

import OpenOPC
import os
import mysql.connector
import time
import datetime

opcserver = 'Matrikon.OPC.Simulation.1'

tags_push_status= ["Square Waves.Int1"]

mydb = mysql.connector.connect(
    host="localhost",
    user="plc_logger",
    passwd="logger123",
    database="pushdb"
    )
cur = mydb.cursor()
opc = OpenOPC.client()
opc.connect(opcserver)
[(opctag1, opcvalue1, opcstat1, opctime1)] = opc.read(tags_push_status,\
                                                      group="g1")
# First run will return 0 record
sqlstring = 'SELECT OVENNO FROM T_PUSH ORDER BY ID DESC LIMIT 1;'
cur.execute(sqlstring)
rows = cur.fetchall()
if len(rows)==0 and opcstat1 == 'Good':
    # print "first run", opcvalue1, opctime1, type(opctime1)
    sqlstring = "INSERT INTO T_PUSH (OVENNO, PUSHTIME)VALUES(%s, %s)"
    now = datetime.datetime.now()
    # convert date in the format you want
    f_now = now.strftime('%Y-%m-%d %H:%M:%S')
    val = (int(opcvalue1), f_now)
    # print val, type(val)
    print sqlstring, val
    res = cur.execute(sqlstring, val)
    mydb.commit()
    time.sleep(10)

try:
    while True:
        [(opctag1, opcvalue1, opcstat1, opctime1)] = opc.read(group="g1")
        sqlstring = 'SELECT OVENNO FROM T_PUSH ORDER BY ID DESC LIMIT 1;'
        cur.execute(sqlstring)
        rows = cur.fetchall()
        print rows
        if opcstat1 == 'Good' and int(rows[0][0]) != opcvalue1:
            print int(rows[0][0]), opcvalue1
            sqlstring = "INSERT INTO T_PUSH (OVENNO, PUSHTIME) \
                VALUES(%s, %s)"
            now = datetime.datetime.now()
            # convert date in the format you want
            f_now = now.strftime('%Y-%m-%d %H:%M:%S')
            val = (int(opcvalue1), f_now)
            print sqlstring, val
            cur.execute(sqlstring, val)
            mydb.commit()
            time.sleep(10)

except KeyboardInterrupt:
    opc.remove('push_status_group')
    opc.close()
    mydb.close()
