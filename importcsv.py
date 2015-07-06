from sys import argv

import csv
import datetime
import sqlite3

conn = sqlite3.connect('schedule.db')
c = conn.cursor()

if len(argv) < 2:
    print "Please provide a name of a csv file. ex: python import_csv.py myfile.csv"
    exit(1)
else:
    csvfile = argv[1]

# Initialize the table

c.execute("CREATE TABLE schedule ( id INTEGER PRIMARY KEY, name TEXT, deadline TIMESTAMP, description TEXT, complete INTEGER )")

schedule = csv.reader(open(csvfile, 'rb'), delimiter=',', quotechar='"')

index = 0
for row in schedule:
    index = index + 1
    print "%s %s" % (index, row)
    c.execute("INSERT INTO schedule VALUES (?, ?, ?, ?, ?)", (index, row[0], datetime.datetime.now()+datetime.timedelta(days=index), row[1], 0))

conn.commit()
conn.close()
exit()
