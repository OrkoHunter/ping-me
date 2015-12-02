#!/usr/bin/python

"""Put GET requests out for ping"""
import MySQLdb as mdb
import datetime
import time

con = mdb.connect('localhost', 'X-X-X', 'X-X-X', 'X-X-X')

while(True):
    t = datetime.datetime.now()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM X-X-X ORDER BY X-X-X;")
        for i in cur.fetchall():
            print i[2] - t
            if i[2] - t < datetime.timedelta(seconds=60) and i[2]>t:
                cur.execute("DELETE FROM X-X-X WHERE X-X-X = \
                            '{}'".format(i[0]))
                f = open("X-X-X", "X-X-X")
                f.write(i[1] + " " + i[3] + "\n")
    time.sleep(55)
