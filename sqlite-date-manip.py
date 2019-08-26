# Written on 24/08/19
# Authors: PA 
# Date manipulation in sqlite
import os
import OpenOPC
import sqlite3
import time

dbfile = 'date_db.db'
opcserver = 'Matrikon.OPC.Simulation.1'

tags_push_status= ["Square Waves.Int1"]
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
sqlstring = 'SELECT VAL FROM T_VAL ORDER BY ID DESC LIMIT 1;'
cur.execute(sqlstring)
rows = cur.fetchall()
if len(rows)==0 and opcstat1 == 'Good':
    print "first run", opcvalue1, opctime1, type(opctime1)
    sqlstring = 'INSERT INTO T_VAL (id, VAL, TIME) \
        VALUES(NULL, "%s", "%s")'%(opcvalue1, opctime1)
    cur.execute(sqlstring)
    db.commit()
    time.sleep(10)

try:
    while True:
        [(opctag1, opcvalue1, opcstat1, opctime1)] = opc.read(group="g1")
        sqlstring = 'SELECT VAL FROM T_VAL ORDER BY ID DESC LIMIT 1;'
        cur.execute(sqlstring)
        rows = cur.fetchall()
        if rows and opcstat1 == 'Good' and int(rows[0][0]) != opcvalue1:
            print int(rows[0][0]), opcvalue1
            sqlstring = 'INSERT INTO T_VAL (id, VAL, TIME) \
                VALUES(NULL, "%s", "%s")'%(opcvalue1, opctime1)
            print opctime1, type(opctime1)
            cur.execute(sqlstring)
            db.commit()
            time.sleep(10)
except KeyboardInterrupt:
    opc.remove('push_status_group')
    opc.close()
    db.close()
    pass



