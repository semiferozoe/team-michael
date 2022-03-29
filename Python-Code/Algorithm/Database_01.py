# import the sql connection library
import sqlite3 as sql
# connect to sql
connect = sql.connect('class_schedule.db')

# Connect to cursor in the databa creation
c= connect.cursor()
c.execute("""create table room (number text, cpacity integer)""")
c.execute("insert into room Values ('Cott 111', 01),"
                                  "('Cott 115', 02),"
                                  "('JoeJ 211', 03),"
                                  "('JoeJ 226', 04)")