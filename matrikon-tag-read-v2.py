# Written on 24/08/19
# Author: Aneesh PA
# The program compares latest data read from plc to the latest data in the
# sqlite database. It writes to db only if the data differ
# Useful if you are periodically poll and log a tag from the controller
# 
# For demo, use Matrikon OPC Explorer to change the Square Wave.Int1 to 0
# and then to a non-zero value;
# Consecutive reads of '0' will not be logged into the database
# Checked on Windows10 64-bit, python 2.7, openopc 

import OpenOPC
import os
import sqlite3
import time

opcserver = 'Matrikon.OPC.Simulation.1'

tags_push_status= ["Square Waves.Int1"]
# db file for push instance
dbfile = 'matri.db'
# checks if dbfile exists
dbexist=os.path.exists(dbfile)
db = sqlite3.connect(dbfile)
cur=db.cursor()
if not dbexist:
    sqlstring = 'CREATE TABLE T_VAL \
    (id INTEGER PRIMARY KEY, \
    VAL TEXT, \
    TIME TEXT)'
    cur.execute(sqlstring)
    db.commit()

opc = OpenOPC.client()
opc.connect(opcserver)
[(opctag1, opcvalue1, opcstat1, opctime1)] = opc.read(tags_push_status,\
                                                      group="g1")
try:
    while True:
        [(opctag1, opcvalue1, opcstat1, opctime1)] = opc.read(group="g1")
        sqlstring = 'SELECT VAL FROM T_VAL ORDER BY ID DESC LIMIT 1;'
        cur.execute(sqlstring)
        rows = cur.fetchall()
        if opcstat1 == 'Good' and int(rows[0][0]) != opcvalue1:
            print int(rows[0][0]), opcvalue1
            sqlstring = 'INSERT INTO T_VAL (id, VAL, TIME) \
                VALUES(NULL, "%s", "%s")'%(opcvalue1, opctime1)
            cur.execute(sqlstring)
            db.commit()
            time.sleep(10)
except KeyboardInterrupt:
    opc.remove('push_status_group')
    opc.close()
    db.close()
    pass


